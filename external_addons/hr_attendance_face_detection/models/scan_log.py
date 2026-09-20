import math

from odoo import api, fields, models


class FaceAttendanceScanLog(models.Model):
    _name = "hr.attendance.face.scan.log"
    _description = "Face Attendance Scan Log"
    _order = "scan_time desc, id desc"
    _rec_name = "scan_time"

    scan_time = fields.Datetime(required=True, default=fields.Datetime.now, index=True)
    user_id = fields.Many2one("res.users", required=True, ondelete="restrict", index=True)
    company_id = fields.Many2one("res.company", required=True, index=True)
    employee_id = fields.Many2one("hr.employee", ondelete="set null", index=True)
    attendance_id = fields.Many2one("hr.attendance", ondelete="set null")
    state = fields.Selection([
        ("pending", "Started / No final result"), ("success", "Success"),
        ("failed", "Failed"), ("cancelled", "Cancelled")], required=True, default="pending", index=True)
    source = fields.Selection([("browser", "Browser"), ("server", "Server")], required=True)
    action = fields.Selection([("check_in", "Check In"), ("check_out", "Check Out")])
    message = fields.Text()
    latitude = fields.Float(digits=(10, 7))
    longitude = fields.Float(digits=(10, 7))
    location_provided = fields.Boolean()
    address = fields.Char()
    response_json = fields.Json(groups="base.group_system")

    matched_location_name = fields.Char(string="Location", readonly=True, index=True)
    location_distance = fields.Float(string="Distance (m)", digits=(12, 2), readonly=True)
    location_match_status = fields.Selection([
        ("matched", "Matched"),
        ("outside", "Outside configured locations"),
        ("no_gps", "No GPS"),
    ], string="Location Status", readonly=True, index=True)

    @api.model
    def _distance_meters(self, lat1, lon1, lat2, lon2):
        lat1, lon1, lat2, lon2 = map(math.radians, (lat1, lon1, lat2, lon2))
        a = (math.sin((lat2 - lat1) / 2) ** 2
             + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2)
        return 6371000 * 2 * math.asin(math.sqrt(max(0, min(1, a))))

    def _snapshot_location(self):
        # Store history, rather than recomputing when location settings change.
        locations_by_company = {}
        for log in self:
            values = {"matched_location_name": False, "location_distance": False,
                      "location_match_status": "no_gps"}
            valid = (log.location_provided
                     and math.isfinite(log.latitude) and math.isfinite(log.longitude)
                     and -90 <= log.latitude <= 90 and -180 <= log.longitude <= 180)
            if valid:
                values["location_match_status"] = "outside"
                if log.company_id.id not in locations_by_company:
                    locations_by_company[log.company_id.id] = self.env["multi.location"].sudo().search(
                        [("company_id", "=", log.company_id.id)], order="id")
                nearest = None
                for location in locations_by_company[log.company_id.id]:
                    lat = location.face_attendance_latitude
                    lon = location.face_attendance_longitude
                    radius = location.face_attendance_radius
                    if not (all(math.isfinite(v) for v in (lat, lon, radius))
                            and -90 <= lat <= 90 and -180 <= lon <= 180 and radius >= 0):
                        continue
                    distance = self._distance_meters(log.latitude, log.longitude, lat, lon)
                    if distance <= radius and (nearest is None or distance < nearest[0]):
                        nearest = (distance, location)
                if nearest is not None:
                    values.update(location_match_status="matched",
                                  matched_location_name=nearest[1].name or "Unnamed location",
                                  location_distance=nearest[0])
            log.write(values)

    @api.model_create_multi
    def create(self, vals_list):
        logs = super().create(vals_list)
        logs._snapshot_location()
        return logs

    def write(self, vals):
        result = super().write(vals)
        if {"latitude", "longitude", "location_provided", "company_id"}.intersection(vals):
            self._snapshot_location()
        return result

    @api.model
    def _backfill_location_snapshots(self):
        # Only missing snapshots: subsequent upgrades preserve recorded history.
        while True:
            logs = self.search([("location_match_status", "=", False)], limit=1000)
            if not logs:
                break
            logs._snapshot_location()

    google_maps_url = fields.Char(string="Google Maps", compute="_compute_map")
    location_map = fields.Html(string="Location Map", compute="_compute_map", sanitize=False)

    @api.depends("latitude", "longitude", "location_provided")
    def _compute_map(self):
        for log in self:
            log.google_maps_url = False
            log.location_map = False
            if not log.location_provided:
                continue
            coordinates = f"{log.latitude:.7f},{log.longitude:.7f}"
            log.google_maps_url = f"https://www.google.com/maps/search/?api=1&query={coordinates}"
            log.location_map = (
                '<iframe title="Scan location" width="100%" height="350" '
                'style="border:0" loading="lazy" referrerpolicy="no-referrer" '
                f'src="https://maps.google.com/maps?q={coordinates}&amp;z=16&amp;output=embed">'
                '</iframe>'
            )

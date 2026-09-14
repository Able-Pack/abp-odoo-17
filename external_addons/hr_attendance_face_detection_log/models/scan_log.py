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
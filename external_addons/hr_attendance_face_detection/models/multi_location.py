# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.
import math
import re
from urllib.parse import parse_qs, unquote, urljoin, urlsplit

import requests

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class MultiLocation(models.Model):
    _name = "multi.location"

    name = fields.Char(help="Check-in or Check-out Area")
    face_attendance_latitude = fields.Float(
        digits=(10, 7),
        help="Company location latitude for face attendance validation"
    )
    face_attendance_longitude = fields.Float(
        digits=(10, 7),
        help="Company location longitude for face attendance validation"
    )
    face_attendance_radius = fields.Float(
        help="Radius setting for face attendance location validation."
             " If set, employees must be within this distance (in meters) "
             "from the company location to mark attendance via face recognition."
    )
    company_id = fields.Many2one('res.company', string="Company", required=True,
                                 ondelete='cascade', default=lambda self: self.env.company)

    map_picker = fields.Boolean(string="Map", store=False)

    google_maps_link = fields.Char(string="Google Maps Link", help="Paste a Google Maps link containing a pinned location or coordinates.")

    @api.model
    def _maps_url(self, value):
        parts = urlsplit(value.strip())
        allowed = {"www.google.com", "google.com", "maps.google.com", "maps.app.goo.gl", "goo.gl"}
        if parts.scheme != "https" or parts.hostname not in allowed or parts.username or parts.password or parts.port not in (None, 443):
            raise ValidationError(_("Use an HTTPS Google Maps link (google.com/maps or maps.app.goo.gl)."))
        if parts.hostname in {"google.com", "www.google.com"} and not parts.path.startswith("/maps"):
            raise ValidationError(_("Please use a Google Maps link."))
        if parts.hostname == "goo.gl" and not parts.path.startswith("/maps/"):
            raise ValidationError(_("Please use a Google Maps link."))
        return parts

    @api.model
    def _coordinates_from_maps_link(self, value):
        current = value.strip()
        parts = self._maps_url(current)
        # Only short Google Maps links need network resolution. Validate every hop.
        if parts.hostname in {"maps.app.goo.gl", "goo.gl"}:
            try:
                with requests.Session() as session:
                    session.trust_env = False
                    for _hop in range(5):
                        parts = self._maps_url(current)
                        if parts.hostname not in {"maps.app.goo.gl", "goo.gl"}:
                            break
                        with session.get(current, allow_redirects=False, timeout=(3, 5), stream=True) as response:
                            if response.status_code not in (301, 302, 303, 307, 308) or not response.headers.get("Location"):
                                raise ValidationError(_("Cannot expand this short link. Open it in your browser and paste the full Google Maps URL."))
                            current = urljoin(current, response.headers["Location"])
                    parts = self._maps_url(current)
            except requests.RequestException as exc:
                raise ValidationError(_("Cannot reach Google Maps. Paste the full URL containing coordinates instead.")) from exc
        text = unquote(current)
        number = r"(-?\d+(?:\.\d+)?)"
        # A place pin takes precedence over the map camera position (@lat,lng).
        match = re.search(r"!3d" + number + r"!4d" + number, text)
        if not match:
            query = parse_qs(parts.query)
            for key in ("query", "q", "ll"):
                values = query.get(key, [])
                match = re.fullmatch(r"\s*" + number + r"\s*,\s*" + number + r"\s*", values[0]) if values else None
                if match:
                    break
        if not match:
            match = re.search(r"/@" + number + r"," + number, text)
        if not match:
            raise ValidationError(_("No coordinates found. Drop a pin in Google Maps and copy its link, or enter latitude and longitude manually."))
        lat, lon = map(float, match.groups())
        if not (math.isfinite(lat) and math.isfinite(lon) and -90 <= lat <= 90 and -180 <= lon <= 180):
            raise ValidationError(_("The Google Maps coordinates are outside the valid range."))
        return {"face_attendance_latitude": lat, "face_attendance_longitude": lon}

    @api.onchange("google_maps_link")
    def _onchange_google_maps_link(self):
        for location in self:
            if location.google_maps_link:
                location.update(location._coordinates_from_maps_link(location.google_maps_link))

    @api.model_create_multi
    def create(self, vals_list):
        values = []
        for vals in vals_list:
            vals = dict(vals)
            if vals.get("google_maps_link"):
                vals.update(self._coordinates_from_maps_link(vals["google_maps_link"]))
            values.append(vals)
        return super().create(values)

    def write(self, vals):
        vals = dict(vals)
        if vals.get("google_maps_link"):
            vals.update(self._coordinates_from_maps_link(vals["google_maps_link"]))
        return super().write(vals)
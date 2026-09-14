from odoo import api, models


class Attendance(models.Model):
    _inherit = "hr.attendance"

    def _link_face_scan_log(self):
        log_id = self.env.context.get("_face_scan_log_id")
        if log_id:
            log = self.env["hr.attendance.face.scan.log"].sudo().browse(log_id).exists()
            if log and log.state == "pending":
                self.ensure_one()
                log.write({"attendance_id": self.id, "employee_id": self.employee_id.id})

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        if self.env.su and self.env.context.get("_face_scan_log_id"):
            records._link_face_scan_log()
        return records

    def write(self, vals):
        result = super().write(vals)
        if "check_out" in vals and self.env.su and self.env.context.get("_face_scan_log_id"):
            self._link_face_scan_log()
        return result

import logging
import math

from odoo import http
from odoo.http import request
from odoo.exceptions import AccessError
from odoo.addons.hr_attendance_face_detection.controllers.main import FaceAttendanceController

_logger = logging.getLogger(__name__)


class FaceScanLogController(FaceAttendanceController):
    def _new_log(self, source):
        return request.env["hr.attendance.face.scan.log"].sudo().create({
            "user_id": request.env.user.id,
            "company_id": request.env.user.company_id.id,
            "source": source,
            "message": "Scan started; no final result received yet.",
        })

    def _owned_log(self, scan_log_id):
        if type(scan_log_id) is not int:
            raise AccessError("Invalid scan log.")
        log = request.env["hr.attendance.face.scan.log"].sudo().browse(scan_log_id).exists()
        if not log or log.user_id.id != request.env.user.id or log.company_id != request.env.user.company_id:
            raise AccessError("Invalid scan log.")
        request.env.cr.execute("SELECT id FROM hr_attendance_face_scan_log WHERE id=%s FOR UPDATE", [log.id])
        log.invalidate_recordset()
        return log

    @http.route("/face_recognition/log/start", type="json", auth="user", methods=["POST"])
    def start_log(self):
        return {"id": self._new_log("browser").id}

    @http.route("/face_recognition/log/finish", type="json", auth="user", methods=["POST"])
    def finish_log(self, scan_log_id, state="failed", message=""):
        log = self._owned_log(scan_log_id)
        if log.state == "pending":
            log.write({
                "state": "cancelled" if state == "cancelled" else "failed",
                "message": str(message)[:2000],
            })
        return True

    def _call_vendor(self, image_data, latitude, longitude):
        return FaceAttendanceController.check_in_out.__wrapped__(
            self, image_data, latitude=latitude, longitude=longitude
        )

    @http.route()
    def check_in_out(self, image_data=None, latitude=None, longitude=None, scan_log_id=None):
        log = self._owned_log(scan_log_id) if scan_log_id is not None else self._new_log("server")
        if log.state != "pending":
            return log.response_json or {"success": False, "msg": "This scan has already ended. Start a new scan."}

        coords = (latitude, longitude)
        valid = all(type(v) in (int, float) and math.isfinite(v) for v in coords)
        valid = valid and -90 <= latitude <= 90 and -180 <= longitude <= 180
        log.write({
            "source": "server", "location_provided": valid,
            "latitude": latitude if valid else False,
            "longitude": longitude if valid else False,
        })
        context = dict(request.env.context)
        try:
            with request.env.cr.savepoint():
                request.update_context(_face_scan_log_id=log.id)
                result = self._call_vendor(image_data, latitude, longitude)
        except Exception:
            _logger.exception("Face attendance scan failed")
            result = {"success": False, "msg": "System error while processing scan."}
        finally:
            request.update_env(context=context)
        log = request.env["hr.attendance.face.scan.log"].sudo().browse(log.id)
        success = bool(result.get("success"))
        log.write({
            "state": "success" if success else "failed",
            "action": result.get("action") if success else False,
            "message": str(result.get("msg", ""))[:2000],
            "address": result.get("location") or False,
            "response_json": result,
        })
        return result

from unittest.mock import patch
from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import AccessError
from odoo.addons.hr_attendance_face_detection.controllers import scan_log as main


class FakeRequest:
    def __init__(self, env):
        self.env = env
    def update_context(self, **values):
        self.env = self.env(context=dict(self.env.context, **values))
    def update_env(self, context):
        self.env = self.env(context=context)


@tagged("post_install", "-at_install")
class TestScanLog(TransactionCase):
    def setUp(self):
        super().setUp()
        self.controller = main.FaceScanLogController()
        self.fake = FakeRequest(self.env)
        self.request_patch = patch.object(main, "request", self.fake)
        self.request_patch.start()
        self.addCleanup(self.request_patch.stop)

    def test_failure_and_browser_finish(self):
        result = {"success": False, "msg": "No matching employee found"}
        with patch.object(self.controller, "_call_vendor", return_value=result):
            self.assertEqual(
                self.controller.check_in_out.__wrapped__(self.controller, "invalid"),
                result,
            )
        log = self.env["hr.attendance.face.scan.log"].search([], limit=1)
        self.assertEqual(log.state, "failed")
        self.assertFalse(log.employee_id)
        scan_id = self.controller.start_log()["id"]
        self.controller.finish_log(scan_id, "failed", "Camera denied")
        log = self.env["hr.attendance.face.scan.log"].browse(scan_id)
        self.assertEqual(log.message, "Camera denied")
        self.controller.finish_log(scan_id, "cancelled", "overwrite")
        self.assertEqual(log.message, "Camera denied")

    def test_success_links_attendance_and_deduplicates(self):
        employee = self.env["hr.employee"].create({"name": "Scan log test employee", "image_1920": False})
        result = {"success": True, "msg": "Checked in", "action": "check_in", "location": "Test"}
        def success(*args, **kwargs):
            self.fake.env["hr.attendance"].sudo().create({"employee_id": employee.id})
            return result
        scan_id = self.controller.start_log()["id"]
        with patch.object(self.controller, "_call_vendor", side_effect=success) as vendor:
            handler = self.controller.check_in_out.__wrapped__
            handler(self.controller, "test", latitude=0, longitude=0, scan_log_id=scan_id)
            self.assertEqual(handler(self.controller, "test", scan_log_id=scan_id), result)
            self.assertEqual(vendor.call_count, 1)
        log = self.env["hr.attendance.face.scan.log"].browse(scan_id)
        self.assertEqual(log.employee_id, employee)
        self.assertTrue(log.attendance_id)
        self.assertEqual(log.state, "success")
        self.assertTrue(log.location_provided)
        self.controller.finish_log(scan_id, "cancelled", "late browser cleanup")
        self.assertEqual(log.state, "success")
        self.assertNotIn("_face_scan_log_id", self.fake.env.context)

    def test_log_ownership_and_permissions(self):
        other = self.env["res.users"].with_context(no_reset_password=True).create({
            "name": "Scan log test user", "login": "scan_log_test_user",
            "groups_id": [(6, 0, [self.env.ref("base.group_user").id])],
        })
        log = self.env["hr.attendance.face.scan.log"].create({
            "user_id": other.id, "company_id": self.env.company.id, "source": "browser",
        })
        with self.assertRaises(AccessError):
            self.controller.finish_log(log.id, "failed", "forged")
        with self.assertRaises(AccessError):
            log.with_user(other).read(["message"])
        officer = self.env.ref("hr_attendance.group_hr_attendance_officer")
        other.write({"groups_id": [(4, officer.id)]})
        self.assertEqual(log.with_user(other).read(["state"])[0]["state"], "pending")
        with self.assertRaises(AccessError):
            log.with_user(other).write({"message": "tamper"})

    def test_location_matching_and_history(self):
        company = self.env["res.company"].create({"name": "Geofence test company"})
        locations = self.env["multi.location"]
        def location(name, lon, radius, company_id=company.id):
            return locations.create({"name": name, "company_id": company_id,
                "face_attendance_latitude": 0, "face_attendance_longitude": lon,
                "face_attendance_radius": radius})
        far = location("Far", 0.002, 500)
        near = location("Near", 0.001, 500)
        location("Closer but outside radius", 0.0001, 1)
        location("Other company", 0, 500, self.env.company.id)
        log = self.env["hr.attendance.face.scan.log"].create({
            "user_id": self.env.user.id, "company_id": company.id, "source": "server",
            "location_provided": True, "latitude": 0, "longitude": 0})
        self.assertEqual(log.matched_location_name, "Near")
        self.assertEqual(log.location_match_status, "matched")
        self.assertAlmostEqual(log.location_distance, 111.195, places=2)
        near.write({"name": "Renamed", "face_attendance_radius": 1})
        near.unlink()
        log.write({"state": "failed"})
        self.assertEqual(log.matched_location_name, "Near")
        log._backfill_location_snapshots()
        self.assertEqual(log.matched_location_name, "Near")
        # Simulate a legacy row for upgrade backfill and its idempotence.
        log.write({"location_match_status": False})
        log._backfill_location_snapshots()
        self.assertEqual(log.matched_location_name, "Far")
        far.unlink()
        log._backfill_location_snapshots()
        self.assertEqual(log.matched_location_name, "Far")
        log.write({"latitude": 10})
        self.assertEqual(log.location_match_status, "outside")
        self.assertFalse(log.matched_location_name)
        log.write({"location_provided": False})
        self.assertEqual(log.location_match_status, "no_gps")
        log.write({"location_provided": True, "latitude": 91})
        self.assertEqual(log.location_match_status, "no_gps")

    def test_location_radius_boundary_and_tie(self):
        company = self.env["res.company"].create({"name": "Boundary test company"})
        logs = self.env["hr.attendance.face.scan.log"]
        radius = logs._distance_meters(0, 0, 0, 0.001)
        values = {"company_id": company.id, "face_attendance_latitude": 0,
                  "face_attendance_longitude": 0.001, "face_attendance_radius": radius}
        self.env["multi.location"].create(dict(values, name="First"))
        self.env["multi.location"].create(dict(values, name="Second"))
        log = logs.create({"user_id": self.env.user.id, "company_id": company.id,
                           "source": "server", "location_provided": True})
        self.assertEqual(log.matched_location_name, "First")
        log.write({"longitude": -0.00001})
        self.assertEqual(log.location_match_status, "outside")
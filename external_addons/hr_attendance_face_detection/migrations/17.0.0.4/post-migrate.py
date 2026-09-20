from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env["hr.attendance.face.scan.log"]._backfill_location_snapshots()
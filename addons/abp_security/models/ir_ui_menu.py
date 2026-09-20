from odoo import api, models, tools


class IrUiMenu(models.Model):
    _inherit = "ir.ui.menu"

    @api.model
    @tools.ormcache('frozenset(self.env.user.groups_id.ids)', 'debug')
    def _visible_menu_ids(self, debug=False):
        visible = set(super()._visible_menu_ids(debug=debug))
        if self.env.user.has_group('abp_security.group_administrator'):
            return visible
        root = self.env.ref('hr_attendance.menu_hr_attendance_root', raise_if_not_found=False)
        face = self.env.ref('hr_attendance_face_detection.menu_face_recognition_root', raise_if_not_found=False)
        if not root:
            return visible
        # Menu visibility only; existing model ACLs and record rules still apply.
        attendance = self.sudo().with_context({'ir.ui.menu.full_list': True}).search([
            ('id', 'child_of', root.id)])
        visible.difference_update(attendance.ids)
        is_face_user = (self.env.user.has_group('abp_security.group_supervisor')
                        or self.env.user.has_group('abp_security.group_salesperson'))
        if is_face_user and root.active and face and face.active:
            visible.update([root.id, face.id])
        return visible
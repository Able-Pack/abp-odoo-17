from odoo import models


class AccountMove(models.Model):
    _inherit = 'account.move'
    
    # Will be called from form view
    def generate_packing_list(self):
        return self.env.ref('abp_packing_list.action_report_packing_list_abp').report_action(self)
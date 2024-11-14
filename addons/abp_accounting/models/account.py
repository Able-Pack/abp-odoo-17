from odoo import api, models


class AccountMove(models.Model):
    _inherit = 'account.move'
    
    @api.model
    def create(self, vals):
        if 'date' in vals:
            vals['invoice_date'] = vals['date']
        return super().create(vals)
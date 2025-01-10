from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'
    
    partner_team_id = fields.Many2one(
        string='Partner Sales Team',
        related='partner_id.team_id',
        store=True
    )
    
    @api.model
    def create(self, vals):
        if 'date' in vals:
            vals['invoice_date'] = vals['date']
        return super().create(vals)
    
    # Will be called from tree views
    def button_print_qrcode(self):
        values = self._prepare_report_values(self)
        return self.env.ref('abp_accounting.action_report_account_move_document_number_qrcode').report_action(self, data={'values': values})
    
    def _prepare_report_values(self, docs):
        values = []
        for doc in docs:
            values.append({
                'document_number': doc.name,
            })
        return values
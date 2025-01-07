from odoo import fields, models


class AccountPayment(models.Model):
    _inherit = 'account.payment'
    
    partner_team_id = fields.Many2one(
        related='partner_id.team_id',
        store=True
    )
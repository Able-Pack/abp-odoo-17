from odoo import models, fields


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    partner_parent_id = fields.Many2one(
        comodel_name='res.partner',
        related='partner_id.parent_id',
        string="Partner's Parent",
        store=True
    )
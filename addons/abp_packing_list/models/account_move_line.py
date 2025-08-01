from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    box_no = fields.Char(string='Box No.', help='Box number for packing list')
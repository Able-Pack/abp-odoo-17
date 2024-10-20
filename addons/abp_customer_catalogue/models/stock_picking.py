import json
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    show_all_product = fields.Boolean(string='Show all products?')
    
    
import json
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    show_all_product = fields.Boolean(string='Show all products?')
    show_base_product = fields.Boolean(string='Show base products?', default=False)
    show_customer_spesific_product = fields.Boolean(string='Show customer-specific products?', default=False)
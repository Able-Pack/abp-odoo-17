import json
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    show_all_product = fields.Boolean(string='Show all products?')
    show_base_product = fields.Boolean(string='Show base products?', default=False)
    show_customer_spesific_product = fields.Boolean(string='Show customer-specific products?', default=False)
    
    def write(self, vals):
        if 'show_base_product' in vals:
            if vals['show_base_product'] == True:
                vals['show_customer_spesific_product'] = False
        if 'show_customer_spesific_product' in vals:
            if vals['show_customer_spesific_product'] == True:
                vals['show_base_product'] = False
                
        return super().write(vals)
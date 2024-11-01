import json
from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'
    
    show_all_product = fields.Boolean(string='Show all products?')
    
    
class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    product_domain = fields.Json(compute='_compute_product_domain')
    
    @api.depends('move_id.partner_id', 'move_id.show_all_product')
    def _compute_product_domain(self):
        for rec in self:
            customer_catalogue = rec.move_id.partner_id.customer_catalogue_ids.mapped('product_id')
            
            if rec.move_id.show_all_product:
                rec.product_domain = json.dumps([])
            else:
                rec.product_domain = json.dumps([('id', 'in', customer_catalogue.ids)])
                
                
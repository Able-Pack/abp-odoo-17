import json
from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'
    
    show_all_product = fields.Boolean(string='Show all products?')
    show_base_product = fields.Boolean(string='Show base products?', default=False)
    show_customer_spesific_product = fields.Boolean(string='Show customer-specific products?', default=False)
    
    
class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    product_domain = fields.Json(compute='_compute_product_domain')
    
    @api.depends('move_id.partner_id', 'move_id.show_all_product', 'move_id.show_base_product', 'move_id.show_customer_spesific_product')
    def _compute_product_domain(self):
        for rec in self:
            if rec.move_id.show_all_product:
                rec.product_domain = json.dumps([('sale_ok', '=', True)])
            elif rec.move_id.show_base_product:
                products = self.env['product.product'].search([]).filtered(lambda x: x.product_tmpl_id.categ_id.display_name.__contains__('AP'))
                rec.product_domain = json.dumps([('id', 'in', products.ids), ('sale_ok', '=', True)])
            elif rec.move_id.show_customer_spesific_product:
                products = self.env['product.product'].search([]).filtered(lambda x: x.product_tmpl_id.categ_id.display_name.__contains__('Customer Specific'))
                rec.product_domain = json.dumps([('id', 'in', products.ids), ('sale_ok', '=', True)])
            elif not rec.move_id.show_all_product and not rec.move_id.show_base_product and not rec.move_id.show_customer_spesific_product:
                customer_catalogue = rec.move_id.partner_id.customer_catalogue_ids.mapped('product_id')
                rec.product_domain = json.dumps([('id', 'in', customer_catalogue.ids), ('sale_ok', '=', True)])
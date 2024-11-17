import json
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class StockMove(models.Model):
    _inherit = 'stock.move'
    
    product_domain = fields.Json(compute='_compute_product_domain')
    
    @api.depends('picking_id.partner_id', 'picking_id.show_all_product', 'picking_id.show_base_product', 'picking_id.show_customer_spesific_product')
    def _compute_product_domain(self):
        for rec in self:
            customer_catalogue = rec.picking_id.partner_id.customer_catalogue_ids.mapped('product_id')
            
            if rec.picking_id.show_all_product:
                rec.product_domain = json.dumps([('sale_ok', '=', True)])
            elif rec.picking_id.show_base_product:
                products = self.env['product.product'].search([]).filtered(lambda x: x.product_tmpl_id.categ_id.display_name.__contains__('AP'))
                rec.product_domain = json.dumps([('id', 'in', products.ids), ('sale_ok', '=', True)])
            elif rec.picking_id.show_customer_spesific_product:
                products = self.env['product.product'].search([]).filtered(lambda x: x.product_tmpl_id.categ_id.display_name.__contains__('Customer Specific'))
                rec.product_domain = json.dumps([('id', 'in', products.ids), ('sale_ok', '=', True)])
            elif not rec.picking_id.show_all_product and not rec.picking_id.show_base_product and not rec.picking_id.show_customer_spesific_product:
                customer_catalogue = rec.picking_id.partner_id.customer_catalogue_ids.mapped('product_id')
                rec.product_domain = json.dumps([('id', 'in', customer_catalogue.ids), ('sale_ok', '=', True)])
                
                
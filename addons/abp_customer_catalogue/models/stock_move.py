import json
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class StockMove(models.Model):
    _inherit = 'stock.move'
    
    product_domain = fields.Json(compute='_compute_product_domain')
    # customer_catalogue_id = fields.Many2one(comodel_name='customer.catalogue')
    # customer_product_code = fields.Char(related='customer_catalogue_id.customer_product_code')
    # customer_product_ref = fields.Char(related='customer_catalogue_id.customer_product_ref')
    # barcode = fields.Char(related='customer_catalogue_id.barcode')
    # retail_price = fields.Float(related='customer_catalogue_id.retail_price')
    
    @api.depends('picking_id.partner_id', 'picking_id.show_all_product', 'picking_id.show_admin_product', 'picking_id.show_base_product', 'picking_id.show_customer_specific_product')
    def _compute_product_domain(self):
        for rec in self:
            if rec.picking_id.show_all_product:
                rec.product_domain = json.dumps([('sale_ok', '=', True)])
                
            elif rec.picking_id.show_admin_product:
                products = self.env['product.product'].search([]).filtered(lambda x: x.product_tmpl_id.categ_id.display_name.__contains__('Admin'))
                rec.product_domain = json.dumps([('id', 'in', products.ids), ('sale_ok', '=', True)])
                
            elif rec.picking_id.show_base_product:
                products = self.env['product.product'].search([]).filtered(lambda x: x.product_tmpl_id.categ_id.display_name.__contains__('AP'))
                rec.product_domain = json.dumps([('id', 'in', products.ids), ('sale_ok', '=', True)])
                
            elif rec.picking_id.show_customer_specific_product:
                products = self.env['product.product'].search([]).filtered(lambda x: x.product_tmpl_id.categ_id.display_name.__contains__('Customer Specific'))
                rec.product_domain = json.dumps([('id', 'in', products.ids), ('sale_ok', '=', True)])
                
            elif not rec.picking_id.show_all_product and not rec.picking_id.show_base_product and not rec.picking_id.show_customer_specific_product:
                customer_catalogue = rec.picking_id.partner_id.customer_catalogue_ids.mapped('product_id')
                rec.product_domain = json.dumps([('id', 'in', customer_catalogue.ids), ('sale_ok', '=', True)])
                
    # @api.onchange('product_id')
    # def _onchange_product_id(self):
    #     customer_catalogue = self.env['customer.catalogue'].search([
    #         ('partner_id', '=', self.partner_id.id),
    #         ('product_id', '=', self.product_id.id),
    #     ], limit=1)
    #     self.customer_catalogue_id = customer_catalogue
        
        
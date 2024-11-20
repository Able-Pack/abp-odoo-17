import json
from lxml import etree
from odoo import api, fields, models
from odoo.addons.abp_utils import views as utils


class AccountMove(models.Model):
    _inherit = 'account.move'
    
    show_all_product = fields.Boolean(string='Show all products?')
    show_base_product = fields.Boolean(string='Show base products?', default=False)
    show_customer_specific_product = fields.Boolean(string='Show customer-specific products?', default=False)
    
    @api.model
    def get_view(self, view_id=None, view_type="form", **options):
        res = super().get_view(view_id, view_type, **options)
        doc = etree.XML(res["arch"])
        
        if view_type in ("form"):
            if not utils.user_has_any_group(self, ['abp_customer_catalogue.group_show_base_product']):
                # Set invisible = True
                utils.set_invisible(doc, True, ["//field[@name='show_base_product']/.."])
                
            if not utils.user_has_any_group(self, ['abp_customer_catalogue.group_show_customer_specific_product']):
                # Set invisible = True
                utils.set_invisible(doc, True, ["//field[@name='show_customer_specific_product']/.."])
                
        res["arch"] = etree.tostring(doc, encoding="unicode")
        return res
    
    def write(self, vals):
        if 'show_base_product' in vals:
            if vals['show_base_product'] == True:
                vals['show_customer_specific_product'] = False
        if 'show_customer_specific_product' in vals:
            if vals['show_customer_specific_product'] == True:
                vals['show_base_product'] = False
                
        return super().write(vals)
    
    
class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    product_domain = fields.Json(compute='_compute_product_domain')
    
    @api.depends('move_id.partner_id', 'move_id.show_all_product', 'move_id.show_base_product', 'move_id.show_customer_specific_product')
    def _compute_product_domain(self):
        for rec in self:
            if rec.move_id.show_all_product:
                rec.product_domain = json.dumps([('sale_ok', '=', True)])
            elif rec.move_id.show_base_product:
                products = self.env['product.product'].search([]).filtered(lambda x: x.product_tmpl_id.categ_id.display_name.__contains__('AP'))
                rec.product_domain = json.dumps([('id', 'in', products.ids), ('sale_ok', '=', True)])
            elif rec.move_id.show_customer_specific_product:
                products = self.env['product.product'].search([]).filtered(lambda x: x.product_tmpl_id.categ_id.display_name.__contains__('Customer Specific'))
                rec.product_domain = json.dumps([('id', 'in', products.ids), ('sale_ok', '=', True)])
            elif not rec.move_id.show_all_product and not rec.move_id.show_base_product and not rec.move_id.show_customer_specific_product:
                customer_catalogue = rec.move_id.partner_id.customer_catalogue_ids.mapped('product_id')
                rec.product_domain = json.dumps([('id', 'in', customer_catalogue.ids), ('sale_ok', '=', True)])
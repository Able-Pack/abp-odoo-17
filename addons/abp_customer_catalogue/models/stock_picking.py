import json
from lxml import etree
from odoo import api, fields, models, _
from odoo.addons.abp_utils import views as utils
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    show_all_product = fields.Boolean(string='Show all products?')
    show_admin_product = fields.Boolean(string='Show admin products?')
    show_base_product = fields.Boolean(string='Show base products?', default=False)
    show_customer_specific_product = fields.Boolean(string='Show customer-specific products?', default=False)
    
    @api.model
    def get_view(self, view_id=None, view_type="form", **options):
        res = super().get_view(view_id, view_type, **options)
        doc = etree.XML(res["arch"])
        
        if view_type in ("form"):
            if not utils.user_has_any_group(self, ['abp_customer_catalogue.group_show_admin_product']):
                # Set invisible = True
                utils.set_invisible(doc, True, ["//field[@name='show_admin_product']/.."])
                
            if not utils.user_has_any_group(self, ['abp_customer_catalogue.group_show_base_product']):
                # Set invisible = True
                utils.set_invisible(doc, True, ["//field[@name='show_base_product']/.."])
                
            if not utils.user_has_any_group(self, ['abp_customer_catalogue.group_show_customer_specific_product']):
                # Set invisible = True
                utils.set_invisible(doc, True, ["//field[@name='show_customer_specific_product']/.."])
                
        res["arch"] = etree.tostring(doc, encoding="unicode")
        return res
    
    def write(self, vals):
        if 'show_admin_product' in vals:
            if vals['show_admin_product'] == True:
                vals['show_base_product'] = vals['show_customer_specific_product'] = False
                
        if 'show_base_product' in vals:
            if vals['show_base_product'] == True:
                vals['show_admin_product'] = vals['show_customer_specific_product'] = False
                
        if 'show_customer_specific_product' in vals:
            if vals['show_customer_specific_product'] == True:
                vals['show_admin_product'] = vals['show_base_product'] = False
                
        return super().write(vals)
    
    @api.onchange('move_ids_without_package')
    def _onchange_move_ids_without_package(self):
        self.show_base_product = False
        self.show_customer_specific_product = False
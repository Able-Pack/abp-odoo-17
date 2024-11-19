from lxml import etree
from odoo import models, api
from odoo.addons.abp_utils import views as utils


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    @api.model
    def get_view(self, view_id=None, view_type="form", **options):
        res = super().get_view(view_id, view_type, **options)
        doc = etree.XML(res["arch"])
        
        if view_type in ("tree", "kanban", "form"):
            if not utils.user_has_any_group(self, ['base.group_system']):
                # Set invisible = True
                utils.set_invisible(doc, True, ["//field[@name='standard_price']"])
                
            if utils.user_has_any_group(self, ['abp_security.abp_group_product_price_readonly']):
                # Set readonly = True
                utils.set_readonly(doc, True, ["//field[@name='list_price']"])
                
            if not utils.user_has_any_group(self, ['abp_security.group_administrator']):
                # Set invisible = True
                utils.set_invisible(doc, True, ["//button", "//field[@name='is_published']"])
                
                # Set options no_open
                utils.set_field_option(doc, ["//field"], no_open=True)
                
                # Set widget falues to empty
                utils.set_empty_widget(doc, ["//field[@name='responsible_id']"])
                
        res["arch"] = etree.tostring(doc, encoding="unicode")
        return res
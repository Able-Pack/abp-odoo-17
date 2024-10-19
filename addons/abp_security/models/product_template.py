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
                
        res["arch"] = etree.tostring(doc, encoding="unicode")
        return res
    
    
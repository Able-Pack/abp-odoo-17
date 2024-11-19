from lxml import etree
from odoo import models, api
from odoo.addons.abp_utils import views as utils


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    @api.model
    def get_view(self, view_id=None, view_type="form", **options):
        res = super().get_view(view_id, view_type, **options)
        doc = etree.XML(res["arch"])
        
        if view_type in ("tree", "kanban", "form"):
            if utils.user_has_any_group(self, ['abp_security.abp_group_purchase_price_readonly']):
                
                # Set readonly = True
                utils.set_readonly(doc, True, ["//field[@name='price_unit']"])
                
        res["arch"] = etree.tostring(doc, encoding="unicode")
        return res
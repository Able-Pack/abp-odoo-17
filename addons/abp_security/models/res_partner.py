from lxml import etree
from odoo import models, api
from odoo.addons.abp_utils import views as utils


class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    @api.model
    def get_view(self, view_id=None, view_type="form", **options):
        res = super().get_view(view_id, view_type, **options)
        doc = etree.XML(res["arch"])
        
        if view_type in ("tree", "kanban", "form"):
            if not utils.user_has_any_group(self, ['base.group_partner_manager']):
                
                # Set no create edit delete
                utils.set_no_create_edit_delete(doc, ['//tree', '//kanban', '//form'], no_create=True, no_edit=True, no_delete=True)
                
        res["arch"] = etree.tostring(doc, encoding="unicode")
        return res
    
    
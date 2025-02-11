from lxml import etree
from odoo import _, models, api
from odoo.addons.abp_utils import views as utils


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    @api.model
    def get_view(self, view_id=None, view_type="form", **options):
        res = super().get_view(view_id, view_type, **options)
        doc = etree.XML(res["arch"])
        
        deliveries_tree_action_id = self.env.ref('stock.action_picking_tree_outgoing').id # deliveries
        if view_type in ("tree", "kanban", "form"):
            if options['action_id'] == deliveries_tree_action_id:
                if utils.user_has_any_group(self, ['abp_security.group_salesperson']):
                    # Set no create edit delete
                    utils.set_no_create_edit_delete(doc, ['//tree', '//kanban', '//form'], no_create=True, no_edit=True, no_delete=True)
                    
        if view_type in ("form"):
            if utils.user_has_any_group(self, ['abp_security.group_administrator']):
                # Set readonly
                utils.set_readonly(doc, False, ["//field[@name='origin']"])
            if utils.user_has_any_group(self, ['abp_security.group_salesperson']):
                # Set domain
                utils.set_domain(doc, ["//field[@name='partner_id']"], "[('team_id', '!=', False)]")
                
        res["arch"] = etree.tostring(doc, encoding="unicode")
        return res
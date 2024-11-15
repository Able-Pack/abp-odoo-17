from odoo import api, models, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    
    @api.depends('picking_type_id', 'partner_id')
    def _compute_location_id(self):
        res = super()._compute_location_id()
        for picking in self:
            if picking.picking_type_id.code == 'internal' and picking.partner_id.location_dest_id:
                picking.location_dest_id = picking.partner_id.location_dest_id
            if picking.picking_type_id.code == 'outgoing' and picking.partner_id.location_src_id:
                picking.location_id = picking.partner_id.location_src_id
                
        return res
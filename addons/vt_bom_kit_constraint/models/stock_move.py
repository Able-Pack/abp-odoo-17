from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class StockMove(models.Model):
    _inherit = "stock.move"
    
    @api.onchange('product_uom_qty')
    def _onchange_product_uom_qty(self):
        incoming = self.picking_id.picking_type_id.code == 'incoming'

        if self.product_uom_qty > self.product_qty_available and not incoming:
            raise ValidationError(_('Demand cannot be greater than on-hand quantity.'))
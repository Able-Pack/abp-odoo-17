from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    product_qty_available = fields.Float('Product On Hand Quantity', related='product_id.qty_available', depends=['product_id'])
    
    @api.onchange('product_uom_qty')
    def _onchange_product_uom_qty(self):
        if self.product_uom_qty > self.product_qty_available:
            raise ValidationError(_('Quantity cannot be greater than on-hand quantity.'))
from odoo import _, api, models
from odoo.exceptions import ValidationError


class StockMove(models.Model):
    _inherit = 'stock.move'
    
    def _update_reserved_quantity(self, need, location_id, quant_ids=None, lot_id=None, package_id=None, owner_id=None, strict=True):
        # If picking is a monthly automated consignment delivery order
        if 'lastcall' in self.env.context: # Use this to make sure it is from scheduled actions (ir.cron)
        # if self.picking_id and self.picking_id.partner_id == self.picking_id.location_id.target_partner_id:
            strict = True
        return super()._update_reserved_quantity(need, location_id, quant_ids=None, lot_id=None, package_id=None, owner_id=None, strict=strict)
    
    @api.constrains('quantity')
    def _constrains_quantity(self):
        for line in self:
            if line.quantity > line.product_uom_qty:
                raise ValidationError(_("Quantity cannot be greater than demand."))
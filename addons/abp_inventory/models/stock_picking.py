import calendar
from datetime import datetime
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
    
    def create_delivery_from_consignment_location(self):
        delivery_location = self.env['stock.location'].search(
            domain=[('is_automated_delivery', '=', True)],
        )
        if not delivery_location:
            return
        
        delivery_order_picking_type = self.env.ref('stock.picking_type_out')
        
        # Create stock picking
        stock_picking = self.env['stock.picking'].create({
            'partner_id': delivery_location.target_partner_id.id,
            'picking_type_id': delivery_order_picking_type.id,
            'location_id': delivery_location.id
        })
        
        stock_quant_consignment = self.env['stock.quant'].search([
            ('location_id', '=', delivery_location.id),
        ])
        # Create stock moves for related picking
        for quant in stock_quant_consignment:
            self.env['stock.move'].create({
                'name': _("Consignment Delivery:") + " %s" % (stock_picking.name),
                'picking_id': stock_picking.id,
                'product_id': quant.product_id.id,
                'product_uom_qty': quant.quantity,
                'location_id': delivery_location.id,
                'location_dest_id': delivery_location.target_partner_id.property_stock_customer.id,
            })
        
        # Validate the picking
        stock_picking.button_validate()
        
    @classmethod
    def get_last_day_of_month(cls):
        today = datetime.today()
        # Get the last day of the current month
        last_day = calendar.monthrange(today.year, today.month)[1]
        return datetime(today.year, today.month, last_day, 23, 59, 59)
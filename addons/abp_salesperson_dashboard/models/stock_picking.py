from odoo import models, api, fields

class Picking(models.Model):
    _inherit = 'stock.picking'

    # Override default picking type based on context
    def _default_picking_type_id_override(self):
        is_non_consignment_return = self.env.context.get('is_non_consignment_return')

        # If the context indicates a non-consignment return, set the picking type accordingly
        if is_non_consignment_return:
            picking_types = self.env['stock.picking.type'].search([
                ('code', '=', 'incoming'),
                ('is_non_consignment', '=', True),
                ('company_id', '=', self.env.company.id),
            ], limit=1)
            
            if picking_types:
                return picking_types.id
        
        return super(Picking, self)._default_picking_type_id()

    # Set the default picking type field to use the override method
    picking_type_id = fields.Many2one(
        default=_default_picking_type_id_override
    )
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class StockLocation(models.Model):
    _inherit = 'stock.location'
    
    
    is_automated_delivery = fields.Boolean()
    target_partner_id = fields.Many2one(comodel_name='res.partner')
    
    @api.constrains('is_automated_delivery')
    def _constrains_is_automated_delivery(self):
        all_stock_location = self.search_read(
            domain=[('is_automated_delivery', '=', True)],
            fields=['id', 'name'],
        )
        if len(all_stock_location) > 1:
            raise ValidationError(_('You cannot have more than one stock location with active automated delivery (location: %s)', [loc['name'] for loc in all_stock_location]))
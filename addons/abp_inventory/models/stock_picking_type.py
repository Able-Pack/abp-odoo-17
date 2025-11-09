from odoo import models, fields, _


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'
    
    is_non_consignment = fields.Boolean(string="Is Non-Consignment", default=False)
    
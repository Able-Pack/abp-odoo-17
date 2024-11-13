from odoo import fields, models, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    def _get_default_consignment_serial(self):
        name = self.env['ir.sequence'].next_by_code('consignment.sequence')
        return name
    
    consignment_serial = fields.Char('Consignment Serial',default=_get_default_consignment_serial)

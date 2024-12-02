from odoo import _, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"
    
    bom_parent_qty = fields.Float(readonly=True)

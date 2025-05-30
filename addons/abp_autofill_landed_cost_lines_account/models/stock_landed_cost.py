from odoo import api, models, _


class StockLandedCostLine(models.Model):
    _inherit = 'stock.landed.cost.lines'
    
    @api.onchange('product_id')
    def onchange_product_id(self):
        super().onchange_product_id()
        self.account_id = self.product_id.property_account_expense_id
from odoo import api, fields, models, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    barcode = fields.Char(string='EAN13')
    
    # Override parent method
    @api.depends('product_id', 'product_uom', 'product_uom_qty')
    def _compute_pricelist_item_id(self):
        for rec in self:
            super()._compute_pricelist_item_id()
            if rec.pricelist_item_id:
                rec.barcode = rec.pricelist_item_id.barcode
                
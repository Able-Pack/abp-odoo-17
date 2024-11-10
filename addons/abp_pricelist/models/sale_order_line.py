from odoo import api, fields, models, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    customer_product_ref = fields.Char(string='Customer Product Ref')
    barcode = fields.Char(string='EAN13')
    retail_price = fields.Monetary(string='Retail Price')
    
    # Override parent method
    @api.depends('product_id', 'product_uom', 'product_uom_qty')
    def _compute_pricelist_item_id(self):
        for rec in self:
            super()._compute_pricelist_item_id()
            if rec.pricelist_item_id:
                rec.customer_product_ref = rec.pricelist_item_id.customer_product_ref
                rec.barcode = rec.pricelist_item_id.barcode
                rec.retail_price = rec.pricelist_item_id.retail_price or rec.pricelist_item_id.fixed_price
                
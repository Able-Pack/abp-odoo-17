from odoo import models, _


class ProductPricelistItem(models.Model):
    _inherit = 'product.pricelist.item'
    
    
    def write(self, vals):
        res = super().write(vals)
        # if 'customer_product_ref' in vals or 'barcode' in vals or 'retail_price' in vals:
        # Trigger recompute on linked customer.catalogue records
        related_catalogues = self.env['customer.catalogue'].search([
            ('pricelist_item_id', 'in', self.ids)
        ])
        related_catalogues._compute_pricelist_item()
        
        return res
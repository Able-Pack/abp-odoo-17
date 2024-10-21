from odoo import api, fields, models, _


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"
    
    
    customer_product_ref = fields.Char()
    
    
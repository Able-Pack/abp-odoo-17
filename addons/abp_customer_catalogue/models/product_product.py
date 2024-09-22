from odoo import fields, models, _


class ProductProduct(models.Model):
    _inherit = "product.product"
    
    customer_catalogue_ids = fields.One2many(comodel_name='customer.catalogue', inverse_name='product_id', string='Customer Catalogues')
    
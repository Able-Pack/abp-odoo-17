from odoo import fields, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    dimension = fields.Char(string='Dimension')
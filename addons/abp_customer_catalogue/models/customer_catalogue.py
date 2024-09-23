from odoo import api, fields, models, _


class CustomerCatalogue(models.Model):
    _name = "customer.catalogue"
    _desc = _name
    
    sequence = fields.Integer(string='Sequence')
    name = fields.Char(string="Name")
    partner_id = fields.Many2one(comodel_name='res.partner', string="Customer", required=True)
    product_tmpl_id = fields.Many2one(comodel_name='product.template', related='product_id.product_tmpl_id')
    product_id = fields.Many2one(comodel_name='product.product', required=True)
    customer_product_code = fields.Char(string='Customer Product Code')
    customer_product_ref = fields.Char(string='Customer Product Ref')
    
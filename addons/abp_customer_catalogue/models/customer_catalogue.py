from odoo import api, fields, models, _


class CustomerCatalogue(models.Model):
    _name = "customer.catalogue"
    _desc = _name
    
    sequence = fields.Integer(string='Sequence')
    name = fields.Char(compute='_compute_name', store=True)
    partner_id = fields.Many2one(comodel_name='res.partner', string="Customer", required=True)
    product_tmpl_id = fields.Many2one(comodel_name='product.template', related='product_id.product_tmpl_id')
    product_id = fields.Many2one(comodel_name='product.product', required=True)
    customer_product_code = fields.Char(string='Customer Product Code')
    customer_product_ref = fields.Char(string='Customer Product Ref')
    
    @api.depends('partner_id', 'product_id', 'customer_product_code', 'customer_product_ref')
    def _compute_name(self):
        for rec in self:
            partner_name = rec.partner_id.name or ''
            product_name = rec.product_tmpl_id.name or ''
            code = rec.customer_product_code or ''
            ref = rec.customer_product_ref or ''
            rec.name = f'{partner_name}-[{product_name}]-{code}-{ref}'
            
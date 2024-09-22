from odoo import api, fields, models, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    customer_catalogue_id = fields.Many2one(comodel_name='customer.catalogue', compute='_compute_customer_catalogue')
    customer_product_code = fields.Char(string='Customer Product Code')
    customer_product_ref = fields.Char(string='Customer Product Ref')
    
    @api.depends('product_template_id', 'order_id.partner_id')
    def _compute_customer_catalogue(self):
        for rec in self:
            customer_catalogue = rec.env['customer.catalogue'].search([
                ('partner_id', '=', rec.order_id.partner_id.id),
                ('product_tmpl_id', '=', rec.product_template_id.id),
            ])
            rec.customer_catalogue_id = customer_catalogue
            if rec.customer_catalogue_id:
                rec.customer_product_code = rec.customer_catalogue_id.customer_product_code
                rec.customer_product_ref = rec.customer_catalogue_id.customer_product_ref
                
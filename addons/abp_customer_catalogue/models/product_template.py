from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    customer_catalogue_ids = fields.One2many(comodel_name='customer.catalogue', inverse_name='product_tmpl_id', string='Customer Catalogues')
    
    # Override name search method to let user search product by customer catalogue's fields
    @api.model
    def _name_search(self, name, domain=None, operator='ilike', limit=None, order=None):
        query = super()._name_search(name, domain, operator, 100, order)
        
        model = self._context.get('model')
        partner_id = self._context.get('partner_id')
        show_all_product = self._context.get('show_all_product')
        if model == 'sale.order' and partner_id and not show_all_product:
            customer_catalogue_ids = self.env['customer.catalogue'].search([
                # '|', '|', '|', # will be used if use customer_product_ref
                '|', '|',
                ('product_tmpl_id.default_code', operator, name),
                ('product_tmpl_id.name', operator, name),
                ('customer_product_code', operator, name),
                # ('customer_product_ref', operator, name),
                ('partner_id', '=', partner_id)
            ])
            additional_product_ids = customer_catalogue_ids.mapped('product_tmpl_id').ids
            
            matching_product_ids = self.env['product.template'].search([('id', 'in', additional_product_ids)]).ids
            if matching_product_ids:
                domain += [('id', 'in', matching_product_ids)]
            else:
                domain += [('id', 'in', [])]
                
            return self._search(domain, limit=limit, order=order)
        
        return query
    
    
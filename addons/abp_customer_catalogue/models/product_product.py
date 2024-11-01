from odoo import api, fields, models, _


class ProductProduct(models.Model):
    _inherit = "product.product"
    
    
    # Override name search method to let user search product by customer catalogue's fields
    @api.model
    def _name_search(self, name, domain=None, operator='ilike', limit=None, order=None):
        query = super()._name_search(name, domain, operator, 100, order)
        
        model = self._context.get('model')
        partner_id = self._context.get('partner_id')
        show_all_product = self._context.get('show_all_product')
        
        if model in ('stock.move', 'account.move') and partner_id and not show_all_product:
            customer_catalogue_ids = self.env['customer.catalogue'].search([
                '|', '|',
                ('product_tmpl_id.default_code', operator, name),
                ('product_tmpl_id.name', operator, name),
                ('customer_product_code', operator, name),
                ('partner_id', '=', partner_id)
            ])
            additional_product_ids = customer_catalogue_ids.mapped('product_id').ids
            
            if additional_product_ids:
                domain += [('id', 'in', additional_product_ids)]
            else:
                domain += [('id', 'in', [])]
                
            return self._search(domain, limit=limit, order=order)
        
        return query
    
    
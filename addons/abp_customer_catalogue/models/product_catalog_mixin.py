from odoo import models, _


class ProductCatalogMixin(models.AbstractModel):
    _inherit = 'product.catalog.mixin'
    
    def _get_product_catalog_additional_domain(self):
        if self._name == 'sale.order':
            order = self
            if not order.show_all_product:
                customer_catalogue = self.env['customer.catalogue'].search([
                    ('partner_id', '=', order.partner_id.id)
                ])
                product_ids = customer_catalogue.mapped('product_id').mapped('id')
                additional_domain = [('id', 'in', product_ids)]
                return additional_domain
            
    def _get_product_catalog_domain(self):
        result = super()._get_product_catalog_domain()
        
        additional_domain = self._get_product_catalog_additional_domain()
        if additional_domain:
            result += additional_domain
            
        return result
    
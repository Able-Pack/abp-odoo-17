from odoo import models


class StockMove(models.Model):
    _inherit = 'stock.move'
    
    # Use customer catalogue fields, but should not depends to abp_customer_catalogue module because of circular dependency
    def _get_customer_catalogue_values(self, partner_id):
        customer_catalogue = partner_id.customer_catalogue_ids.filtered(lambda x: x.product_id == self.product_id)
        values = {
            'customer_product_code': customer_catalogue.customer_product_code,
            'customer_product_ref': customer_catalogue.customer_product_ref,
            'retail_price': customer_catalogue.retail_price,
        }
        return values
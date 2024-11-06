from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"
    
    # Use customer catalogue fields, but should not depends to abp_customer_catalogue module because of circular dependency
    def _get_customer_catalogue_values(self, partner_id, product_id):
        customer_catalogue = partner_id.customer_catalogue_ids.filtered(lambda self: self.product_id == product_id)
        values = {
            'customer_product_code': customer_catalogue.customer_product_code,
            'customer_product_ref': customer_catalogue.customer_product_ref,
        }
        return values
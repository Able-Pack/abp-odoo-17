from odoo import models, api, _, fields
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_product = fields.Boolean(string='product', compute='_compute_product_price_lock')

    def _compute_product_price_lock(self):
        for rec in self:
            if self.env.user.has_group('eg_all_in_one_lock_price.product_price_readonly'):
                rec.is_product = True
            else:
                rec.is_product = False

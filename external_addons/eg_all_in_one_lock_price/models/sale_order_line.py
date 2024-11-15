from odoo import models, api, _, fields
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_sale = fields.Boolean(string='Sale', compute='_compute_is_sale')
    price_unit = fields.Float(string='Price unit')

    def _compute_is_sale(self):
        for rec in self:
            if self.env.user.has_group('eg_all_in_one_lock_price.sale_price_readonly'):
                rec.is_sale = True
            else:
                rec.is_sale = False

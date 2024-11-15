from odoo import models, api, _, fields
from odoo.exceptions import UserError


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    is_purchase = fields.Boolean(string='purchase', compute='compute_purchase_price_lock')
    price_unit = fields.Float(string='Price unit')

    def compute_purchase_price_lock(self):
        for rec in self:
            if self.env.user.has_group('eg_all_in_one_lock_price.purchase_price_readonly'):
                rec.is_purchase = True
            else:
                rec.is_purchase = False

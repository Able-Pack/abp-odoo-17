from odoo import _, models


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'
    
    def create_invoices(self):
        res = super().create_invoices()
        for order in self.sale_order_ids:
            order._create_customer_catalogue()
            if order.has_new_customer_catalogue:
                order.button_notify_catalogue_creation()
        return res
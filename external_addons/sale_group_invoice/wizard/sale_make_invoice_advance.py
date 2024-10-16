# Copyright 2021-2023 Sodexis
# License OPL-1 (See LICENSE file for full copyright and licensing details).

from odoo import api, fields, models


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    summary = fields.Boolean(
        string="Create summary invoice for selected orders only", default=True
    )
    individual = fields.Boolean(string="Create summary invoice for all billable orders")

    @api.onchange("summary")
    def _onchange_select_summarytype(self):
        if self.summary and self.individual:
            if self.individual:
                self.individual = False

    @api.onchange("individual")
    def _onchange_select_individualtype(self):
        if self.summary and self.individual:
            if self.summary:
                self.summary = False

    def create_invoices(self):
        if self.individual:
            active_ids = self.env.context.get("active_ids", [])
            sale = self.env["sale.order"].browse(active_ids)
            customer_ids = sale.mapped("partner_id").ids
            so_records = (
                self.env["sale.order"]
                .search([("partner_id", "in", customer_ids)])
                .filtered(lambda so: so.invoice_status == "to invoice")
            )
            self.sale_order_ids = so_records
        return super(
            SaleAdvancePaymentInv, self.with_context(from_create_invoice=True)
        ).create_invoices()

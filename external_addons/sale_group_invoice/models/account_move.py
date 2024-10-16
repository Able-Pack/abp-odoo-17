# Copyright 2021-2023 Sodexis
# License OPL-1 (See LICENSE file for full copyright and licensing details).

from odoo import api, models


class AccountInvoice(models.Model):
    _inherit = "account.move"

    @api.model_create_multi
    def create(self, vals_list):
        if self._context.get("from_create_invoice", False):
            for vals in vals_list:
                invoice_line_ids = vals.get("invoice_line_ids", [])

                dict_val = {}
                temp = []
                index_val = 0

                for line_vals in invoice_line_ids:
                    if "display_type" in line_vals[2] and line_vals[2].get(
                        "display_type"
                    ) not in ["line_section", "line_note"]:
                        sale_line_id = False
                        if line_vals[2].get("sale_line_ids"):
                            if line_vals[2].get("sale_line_ids")[0][0] == 6:
                                sale_line_id = line_vals[2].get("sale_line_ids")[0][2]
                            elif line_vals[2].get("sale_line_ids")[0][0] == 4:
                                sale_line_id = line_vals[2].get("sale_line_ids")[0][1]

                        if sale_line_id:
                            sale_id = (
                                self.env["sale.order.line"]
                                .browse(sale_line_id)
                                .order_id
                            )
                            if sale_id.name not in dict_val:
                                dict_val[sale_id.name] = [
                                    index_val,
                                    line_vals[2].get("sequence"),
                                ]
                                index_val += 1
                index_val = 0
                for key, val in dict_val.items():
                    temp.append(
                        (
                            0,
                            0,
                            {
                                "name": key,
                                "quantity": 1.0,
                                "discount": 0.0,
                                "display_type": "line_section",
                                "sequence": val[1],
                            },
                        )
                    )

                vals["invoice_line_ids"] = temp + invoice_line_ids
                index_val += 1
        return super().create(vals_list)

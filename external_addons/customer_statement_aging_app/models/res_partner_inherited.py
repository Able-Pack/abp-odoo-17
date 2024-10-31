# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ResPartnerInherit(models.Model):
    _inherit = "res.partner"

    def action_open_wizard(self):
        return {
            'name': 'Customer Statement Report',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            "view_type": "form",
            'res_model': 'customer.statement.wizard',
            'target': 'new',
            'view_id': self.env.ref('customer_statement_aging_app.customer_statement_wizard_form_view').id,
            'context': self._context,
        }


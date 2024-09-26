# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.


from odoo import fields, models, _


class HrPayslipInherit(models.Model):
    _inherit = 'hr.payslip'

    payslip_commission = fields.Float(
        string='Commission', compute="_payslip_commission_count")

    def _payslip_commission_count(self):
        for rec in self:
            rec.payslip_commission = 0.0
            if rec.date_to and rec.date_from and rec.employee_id and rec.employee_id.user_id:
                sale_order = self.env['sale.order'].sudo().search([('date_order', '>=', rec.date_from), (
                    'date_order', '<=', rec.date_to), ('state', '=', 'sale'), ('user_id', '=', rec.employee_id.user_id.id)])
                if sale_order:
                    rec.payslip_commission = sum(sale_order.mapped('price_commission'))

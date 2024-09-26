# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.


from odoo import fields, models, _


class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    sale_target_ids = fields.Many2one('target.group', string='Sale Target')
    commission = fields.Float(string="Commission (%)")
    commission_count = fields.Float(
        string='Overall Commission', compute="_compute_commission")
    sale_count = fields.Float(string='Total Sale', compute="_compute_sale")

    def _find_commission_count(self, payslip):
            return payslip.payslip_commission

    def _compute_commission(self):
        for rec in self:
            rec.commission_count = 0.0
            if rec.user_id:
                sale_order = self.env['sale.order'].sudo().search(
                    [('user_id', '=', rec.user_id.id), ('state', '=', 'sale')])
                if sale_order:
                    rec.commission_count = sum(
                        sale_order.mapped('price_commission'))

    def _compute_sale(self):
        for rec in self:
            rec.sale_count = 0
            if rec.user_id:
                sale_order = self.env['sale.order'].sudo().search(
                    [('user_id', '=', rec.user_id.id), ('state', '=', 'sale')])
                if sale_order:
                    rec.sale_count = sum(sale_order.mapped('amount_total'))

    def commission_sale_info(self):
        return {
            'name': _('Commission'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'domain': [],
            'res_model': 'target.group',
            'type': 'ir.actions.act_window',
            'target': 'self',
        }

    def total_sale_info(self):
        return {
            'name': _('Sales Orders'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'domain': [('user_id', '=', self.user_id.id)],
            'res_model': 'sale.order',
            'type': 'ir.actions.act_window',
            'target': 'self',
        }

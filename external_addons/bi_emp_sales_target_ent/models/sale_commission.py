# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    target_group_id = fields.Many2one(comodel_name='target.group', compute='_compute_target_group', string='Commission Group', store=True)
    price_commission = fields.Float(compute="_compute_commission_price", string='Commission')
    
    @api.depends('user_id')
    def _compute_target_group(self):
        for rec in self:
            target_group = self.env['target.group'].search([
                ('target_id.sale_name_id', '=', rec.user_id.id),
                ('start_date', '<=', rec.date_order),
                ('end_date', '>=', rec.date_order),
            ], limit=1)
            rec.target_group_id = target_group

    @api.depends('amount_untaxed', 'target_group_id', 'user_id')
    def _compute_commission_price(self):
        for rec in self:
            price_subtotal = 0.0
            if rec.target_group_id:
                target_lines_id = self.env['target.lines'].sudo().search(
                    [('target_group_id', '=', rec.target_group_id.id), ('min_target', '<=', rec.amount_untaxed), ('max_target', '>=', rec.amount_untaxed)], limit=1)
                if target_lines_id:
                    if rec.target_group_id.commission_type == 'amount' and rec.user_id in rec.target_group_id.target_id.sale_name_id:
                        price_subtotal = target_lines_id.amount
                    else:
                        price_subtotal = rec.amount_untaxed * ((target_lines_id.amount_percentage) / 100)
            rec.price_commission = price_subtotal

# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.


from odoo import fields, models, api, _
from odoo.exceptions import UserError


class TargetGroup(models.Model):
    _name = 'target.group'
    _description = "Sale Target Group"

    name = fields.Char(string='Name', required=True)
    commission_type = fields.Selection(
        [('amount', 'Amount'), ('percentage', 'Percentage')], 'Commission Type', default='amount')
    target_lines = fields.One2many('target.lines', 'target_group_id')
    target_id = fields.One2many(
        'target.commission.lines', 'target_line_id', string='Sale Person')
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)


class TargetLine(models.Model):
    _name = 'target.lines'
    _description = 'Sale Target Lines'

    target_group_id = fields.Many2one('target.group')
    min_target = fields.Float(string='Min Target')
    max_target = fields.Float(string='Max Target')
    amount = fields.Float(string='Commission Amount')
    amount_percentage = fields.Float(string="Commission Percentage(%)")

    @api.constrains('min_target')
    def _check_target(self):
        for rec in self:
            if rec.min_target > rec.max_target:
                raise UserError(_('Max Target Can Not Less Than Min Target.'))

    @api.constrains('amount_percentage')
    def _check_percentage(self):
        for rec in self:
            if rec.amount_percentage >= 100:
                raise UserError(_('Can Not Added More than 100%.'))


class TargetCommissionLines(models.Model):
    _name = 'target.commission.lines'
    _description = 'Target Commission Lines'

    target_line_id = fields.Many2one(
        'target.group',  string='Target commissionn')
    sale_name_id = fields.Many2one(
        'res.users', string='Name', default=lambda self: self.env.user)

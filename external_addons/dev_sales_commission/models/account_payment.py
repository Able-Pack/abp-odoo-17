# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solutionaccount_payment
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime

class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'
    
    @api.model
    def _get_default_team(self):
        return self.env['crm.team']._get_default_team_id()
        
    user_id = fields.Many2one('res.users', string='Salesperson', index=True, default=lambda self: self.env.user)
    team_id = fields.Many2one('crm.team', string='Sales Team', change_default=True, default=_get_default_team)
    
    def _create_payment_vals_from_wizard(self, first_batch_result):
        res = super(AccountPaymentRegister,self)._create_payment_vals_from_wizard(first_batch_result)
        res.update({
            'user_id':self.user_id and self.user_id.id or False,
            'team_id':self.team_id and self.team_id.id or False,
        })
        return res

class account_payment(models.Model):
    _inherit = "account.payment"
    
    @api.model
    def _get_default_team(self):
        return self.env['crm.team']._get_default_team_id()
        
    user_id = fields.Many2one('res.users', string='Salesperson', index=True, default=lambda self: self.env.user)
    team_id = fields.Many2one('crm.team', string='Sales Team', change_default=True, default=_get_default_team)
    
    commission_line_ids = fields.Many2many('sale.commission.line', string='Commission Lines', copy=False)
    commission_count = fields.Integer('Count Commission', compute='_get_commission_count')
    
    @api.depends('commission_line_ids')
    def _get_commission_count(self):
        for payment in self:
            payment.commission_count = len(self.commission_line_ids.ids)
            
    def action_view_commission(self):
        commissions = self.mapped('commission_line_ids')
        action = self.env.ref('dev_sales_commission.action_sale_commission_line').read()[0]
        if len(commissions) > 1:
            action['domain'] = [('id', 'in', commissions.ids)]
        elif len(commissions) == 1:
            form_view = [(self.env.ref('dev_sales_commission.view_dev_sale_commission_line_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = commissions.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action
        
    
    def generate_lines(self,user,user_type,amount):
        vals ={
            'date':datetime.now(),
            'user_type':user_type,
            'user_id':user and user.id or False,
            'amount':amount,
            'currency_id':self.company_id.currency_id and self.company_id.currency_id.id or False,
            'origin':self.name or '',
            'company_id':self.company_id and self.company_id.id or False,
        }
        line_id = self.env['sale.commission.line'].create(vals)
        line_ids = self.commission_line_ids.ids or []
        if line_id:
            line_ids.append(line_id.id)
        self.commission_line_ids = [(6,0, line_ids)]
        
    def generate_commission_on_sale_team(self):
        compny_currency_id = self.company_id.currency_id
        currency_id = self.currency_id
        team_id = self.team_id
        amount = self.amount
        if compny_currency_id.id != currency_id.id:
            currency_id = currency_id.with_context(date=self.date_invoice)
            amount = currency_id.compute(amount, compny_currency_id)
        if team_id and team_id.commission_config_lines:
            saleperson_commission = 0.0
            manager_commission = 0.0
            for line in team_id.commission_config_lines:
                if line.from_amount <= amount and line.to_amount >= amount:
                    if team_id.commission_type == 'fix_amount':
                        saleperson_commission = line.salesperson_amount
                        manager_commission = line.manager_amount
                    else:
                        saleperson_commission = (amount * line.salesperson_per)/100
                        manager_commission = (amount * line.manager_per)/100
                    break
                    
            manager_id = False
            salesperson = False
            if team_id.user_id:
                manager_id = team_id.user_id
            if self.user_id and self.user_id.id != manager_id.id:
                salesperson = self.user_id
            if saleperson_commission and salesperson:
                self.generate_lines(salesperson,'sale_person',saleperson_commission)
            if manager_commission and manager_id:
                self.generate_lines(manager_id,'sale_manager',manager_commission)
                
    
    def generate_payment_commission(self):
        if self.company_id.calculation_base_on == 'sale_team':
            self.generate_commission_on_sale_team()
            
            
    def action_post(self):
        print ("=======",self.company_id.commission_pay, self.partner_type, self.payment_type)
        res = super(account_payment,self).action_post()
        if self.partner_type == 'customer' and self.payment_type == 'inbound':
            if self.company_id.commission_pay == 'customer_payment':
                for payment in self:
                    payment.generate_payment_commission()
        return res
    

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:


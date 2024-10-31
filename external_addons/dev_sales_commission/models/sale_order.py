# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime


class sale_order(models.Model):
    _inherit = "sale.order"
    
    commission_line_ids = fields.Many2many('sale.commission.line', string='Commission Lines', copy=False)
    commission_count = fields.Integer('Count Commission', compute='_get_commission_count')
    
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
        
    
    @api.depends('commission_line_ids')
    def _get_commission_count(self):
        for sale in self:
            sale.commission_count = len(self.commission_line_ids.ids)
    
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
        amount = self.amount_untaxed
        if compny_currency_id.id != currency_id.id:
            currency_id = currency_id.with_context(date=self.date_order)
            amount = currency_id.compute(amount, compny_currency_id)
        if team_id.commission_config_lines:
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
                print("========  if condition 1 =================")
            if self.user_id and self.user_id.id != manager_id.id:
                salesperson = self.user_id
                print("========  if condition 2 =================")
            if saleperson_commission and salesperson:
                self.generate_lines(salesperson,'sale_person',saleperson_commission)
                print("========  if condition 3 =================")
            if manager_commission and manager_id:
                self.generate_lines(manager_id,'sale_manager',manager_commission)
                print("========  if condition 4 =================")
        print("=======Generate by sale team ============================")        
    
    def generate_commission_on_product_category(self):
        compny_currency_id = self.company_id.currency_id
        currency_id = self.currency_id
        team_id = self.team_id
        saleperson_commission = 0.0
        manager_commission = 0.0
        for order_line in self.order_line:
            categ_id = order_line.product_id and order_line.product_id.categ_id
            if categ_id and categ_id.commission_config_lines and categ_id.commission_type:
                amount = order_line.price_subtotal
                if compny_currency_id.id != currency_id.id:
                    currency_id = currency_id.with_context(date=self.date_order)
                    amount = currency_id.compute(amount, compny_currency_id)
                match = False
                for line in categ_id.commission_config_lines:
                    if not match:
                        if line.from_amount <= amount and line.to_amount >= amount:
                            match = True
                            if categ_id.commission_type == 'fix_amount':
                                saleperson_commission += line.salesperson_amount
                                manager_commission += line.manager_amount
                            else:
                                saleperson_commission += (amount * line.salesperson_per)/100
                                manager_commission += (amount * line.manager_per)/100
        
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
                        
    
    def generate_commission_on_product(self):
        compny_currency_id = self.company_id.currency_id
        currency_id = self.currency_id
        team_id = self.team_id
        saleperson_commission = 0.0
        manager_commission = 0.0
        for order_line in self.order_line:
            product_id = order_line.product_id
            if product_id and product_id.is_commission_product and product_id.commission_config_lines and product_id.commission_type:
                amount = order_line.price_subtotal
                if compny_currency_id.id != currency_id.id:
                    currency_id = currency_id.with_context(date=self.date_order)
                    amount = currency_id.compute(amount, compny_currency_id)
                match = False
                for line in product_id.commission_config_lines:
                    if not match:
                        if line.from_amount <= amount and line.to_amount >= amount:
                            match = True
                            if product_id.commission_type == 'fix_amount':
                                saleperson_commission += line.salesperson_amount
                                manager_commission += line.manager_amount
                            else:
                                saleperson_commission += (amount * line.salesperson_per)/100
                                manager_commission += (amount * line.manager_per)/100
        
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
            
    
    def generate_sale_confirm_commission(self):
        if self.company_id.calculation_base_on == 'sale_team':
            self.generate_commission_on_sale_team()
        elif self.company_id.calculation_base_on == 'product_category':
            self.generate_commission_on_product_category()
        elif self.company_id.calculation_base_on == 'product':
            self.generate_commission_on_product()
            
            
    
    def action_confirm(self):
        res = super(sale_order,self).action_confirm()
        if self.company_id.commission_pay == 'sale_confirm':
            self.generate_sale_confirm_commission()
        print("============= Confrim Done=========================")
        return res
    

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:


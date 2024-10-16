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
import calendar

class sale_commission(models.Model):
    _name = 'sale.commission'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Sale Commission'
    _order = 'name desc'
    
    @api.model
    def _get_to_date(self):
        date = datetime.now()
        m_range = calendar.monthrange(date.year,date.month)
        month = date.month
        if date.month < 10:
            month = '0'+str(date.month)
        date = str(date.year)+'-'+str(month)+'-'+str(m_range[1])
        return date
    
    name = fields.Char('Name', default='/', copy=False)
    end_date = fields.Date('To Date', required="1", default=_get_to_date)
    date = fields.Date('Date', required="1", default=fields.Date.today())
    amount = fields.Monetary('Amount', compute='_get_amount', tracking=1)
    currency_id = fields.Many2one('res.currency', string='Currency', required="1", default=lambda self:self.env.user.company_id.currency_id)
    state = fields.Selection([('draft','Draft'),('confirm','Confirm'),('paid','Paid'),('cancel','Cancel')], 
                                string='State', default='draft', tracking=2)
    company_id = fields.Many2one('res.company', string='Company',  default=lambda self:self.env.user.company_id, required="1")
    commission_lines = fields.One2many('sale.commission.line', 'commission_id', string='Commission Lines')
    user_id = fields.Many2one('res.users', string='Sales Person', required="1", tracking=2)
    invoice_id = fields.Many2one('account.move', string='Invoice', copy=False)
    invoice_count = fields.Integer('Invoice Count', compute='_get_invoice_count')
    invisible_create_invoice = fields.Boolean('Invisible Create Invoice',compute='_check_commission_invoice')
    
    
    @api.depends('invoice_id','invoice_id.state')
    def _check_commission_invoice(self):
        for com in self:
            com.invisible_create_invoice = False
            if com.invoice_id:
                if com.invoice_id.state != 'cancel':
                    com.invisible_create_invoice = True
    
    
    @api.depends('invoice_id')
    def _get_invoice_count(self):
        for com in self:
            if com.invoice_id:
                com.invoice_count = 1
            else:
                com.invoice_count = 0
    
    def action_view_invoice(self):
        action = self.env.ref('account.action_move_in_invoice_type')
        result = action.read()[0]
        res = self.env.ref('account.view_move_form', False)
        form_view = [(res and res.id or False, 'form')]
        if 'views' in result:
            result['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
        else:
            result['views'] = form_view
        result['res_id'] = self.invoice_id.id or False
        return result
        
    
    @api.depends('commission_lines')
    def _get_amount(self):
        for commission in self:
            amount = 0
            for line in commission.commission_lines:
                amount += line.amount
            commission.amount = amount
            
    
 #   @api.model_create_multi
 #   def create(self, vals):
        #if vals.get('name',  '/') == '/':
 #       vals['name'] = self.env['ir.sequence'].sudo().next_by_code(
  #              'sale.commission') or '/'
   #     return super(sale_commission, self).create(vals)
     
    @api.model
    def create(self,vals):
        vals['name']=self.env['ir.sequence'].sudo().next_by_code('sale.commission') or 'New'
        res = super(sale_commission,self).create(vals)
        return res   
    
    def unlink(self):
        for commission in self:
            if commission.state not in ('draft', 'cancel'):
                raise ValidationError(_('Sale Commission delete on draft and cancel state.'))
        return super(sale_commission, self).unlink()
    
    def action_load_lines(self):
        for line in self.commission_lines:
            line.commission_id = False
             
        line_ids = self.env['sale.commission.line'].search([('user_id','=',self.user_id.id),('commission_id','=',False),('state','=','draft'),('date','<=',self.end_date)])
        for line in line_ids:
            line.commission_id = self.id
    
    def action_cancel(self):
        if self.invoice_id and self.invoice_id.state != 'cancel':
            raise ValidationError(_('First Cancel the invoice then after cancel sale commission.'))
        else:
            for line in self.commission_lines:
                line.commission_id = False
            self.state = 'cancel'
            
    def action_confirm(self):
        self.action_load_lines()
        self.state = 'confirm'
        
    def action_commission_paid(self):
        if self.invoice_id.payment_state != 'paid':
            raise ValidationError(_('Please Pay commission invoice.'))
        self.state = 'paid'
        for line in self.commission_lines:
            line.state = 'paid'
        
    def set_to_draft(self):
        self.state = 'draft'
    
    def _prepare_invoice_line(self,invoice_id):
        self.ensure_one()
        res = {}
        if not self.company_id.product_id:
            raise ValidationError(_('Please define Commission product in sale setting.'))
            
        account = self.company_id.product_id.property_account_expense_id or self.company_id.product_id.categ_id.property_account_expense_categ_id
        if not account and self.product_id:
            raise ValidationError(_('Please define expense account for this product: "%s" (id:%d) - or for its category: "%s".') %
                (self.company_id.product_id.name, self.company_id.product_id.id, self.company_id.product_id.categ_id.name))

        res = {
            'name': self.company_id.product_id.name,
            'account_id': account and account.id,
            'price_unit': self.amount,
            'quantity': 1,
            'product_uom_id': self.company_id.product_id and self.company_id.product_id.uom_id and self.company_id.product_id.uom_id.id,
            'product_id': self.company_id.product_id.id or False,
        }
        return res
    
    def _prepare_invoice(self):
        self.ensure_one()
        journal_id = self.env['account.journal'].search([('company_id','=',self.company_id.id),('type','=','purchase')],limit=1)
        if not journal_id:
            raise ValidationError(_('Please define accounting Purchase journal for this company.'))
        partner_id = self.user_id.partner_id
        invoice_vals = {
            'invoice_origin': self.name,
            'move_type': 'in_invoice',
#            'account_id': partner_id.property_account_payable_id.id,
            'partner_id': partner_id.id,
            'partner_shipping_id': partner_id.id,
            'journal_id': journal_id and journal_id.id or False,
            'currency_id': self.currency_id.id,
            'company_id': self.company_id.id,
        }
        return invoice_vals
        
    
    def action_create_invoice(self):
        if self.amount:
            inv_vals = self._prepare_invoice()
            invoice_id = self.env['account.move'].sudo().create(inv_vals)
            if invoice_id:
                vals = []
                vals.append((0,0,self._prepare_invoice_line(invoice_id)))
                invoice_id.invoice_line_ids = vals
                self.invoice_id = invoice_id and invoice_id.id or False
    
            

class sale_commission_lines(models.Model):
    _name = "sale.commission.line"
    _description = 'Sale Commission Lines'
    _rec_name = 'user_id'
    
    date = fields.Date('Date', required="1")
    user_type = fields.Selection([('sale_person','Sales Person'),('sale_manager','Sales Manager')], string='User Type')
    user_id = fields.Many2one('res.users', string='Sales Person', required="1")
    currency_id = fields.Many2one('res.currency', string='Currency')
    amount = fields.Monetary('Amount')
    origin = fields.Char('Source Document')
    is_paid = fields.Boolean('IS Paid')
    company_id = fields.Many2one('res.company', string='Company',  default=lambda self:self.env.user.company_id, required="1")
    commission_id = fields.Many2one('sale.commission', string='Sale Commission')
    state = fields.Selection([('draft','Draft'),('paid','Paid')], string='State', default='draft', copy=False)
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:


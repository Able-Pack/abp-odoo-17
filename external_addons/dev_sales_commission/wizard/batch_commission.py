# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle 
#
##############################################################################

from odoo import api, fields, models, _
from datetime import datetime,date
import calendar
import itertools
from operator import itemgetter
import operator
from odoo.exceptions import ValidationError
import calendar

class dev_batch_sales_commission(models.TransientModel):
    _name = "dev.batch.sales.commission"
    _description = 'Batch sales Commission'
    
    @api.model
    def _get_to_date(self):
        date = datetime.now()
        m_range = calendar.monthrange(date.year,date.month)
        month = date.month
        if date.month < 10:
            month = '0'+str(date.month)
        date = str(date.year)+'-'+str(month)+'-'+str(m_range[1])
        return date
    
    end_date = fields.Date('To Date', required="1", default=_get_to_date)
    user_ids = fields.Many2many('res.users', string='Salesperson')
    
    
    def action_create_sales_commission(self):
        commission_ids = []
        for user in self.user_ids:
            line_ids = self.env['sale.commission.line'].search([('user_id','=',user.id),
                                                                ('commission_id','=',False),
                                                                ('state','=','draft'),
                                                                ('date','<=',self.end_date)])
            if line_ids:
                vals={
                    'user_id':user.id or False,
                    'end_date':self.end_date,
                    'date':date.today(),
                    'currency_id':self.env.user.company_id.currency_id.id or False,
                    'company_id':self.env.user.company_id.id or False,
                }
                commission = self.env['sale.commission'].sudo().create(vals)
                commission.action_load_lines()
                commission_ids.append(commission.id)
       
        if commission_ids:
            action = self.env.ref('dev_sales_commission.action_sale_commission').read()[0]
            action['domain'] = [('id', 'in', commission_ids)]
            return action
                
            
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:    
    

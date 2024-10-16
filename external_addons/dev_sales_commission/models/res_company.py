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


class res_company(models.Model):
    _inherit = "res.company"
    
    commission_pay = fields.Selection([('sale_confirm','Sales Confirmation'),
                                       ('invoice_validate','Invoice Validate'),
                                       ('customer_payment','Customer Payment')], default='sale_confirm', string='Commission Pay')
    
    calculation_base_on = fields.Selection([('sale_team','Sales Team'),
                                       ('product_category','Product Category'),
                                       ('product','Product')], default='sale_team', string='Calculation Based on')
    
    product_id = fields.Many2one('product.product', string='Product')
    

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:


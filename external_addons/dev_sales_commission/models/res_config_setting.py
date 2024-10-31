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


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    commission_pay = fields.Selection(string="When to Pay", related='company_id.commission_pay', readonly=False)
    
    calculation_base_on = fields.Selection(string="Calculation Based On", 
                                           related='company_id.calculation_base_on',
                                           readonly=False)
    
    product_id = fields.Many2one(related='company_id.product_id', string='Commission Product', readonly=False)
                                       
    

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

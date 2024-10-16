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


class product_category(models.Model):
    _inherit = "product.category"
    
    commission_type = fields.Selection([('fix_amount','Fix Amount'),('percentage','By Percentage')], string='Commission Type')
    commission_config_lines = fields.One2many('commission.config.lines','categ_id', string='Commission Lines')
    

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:


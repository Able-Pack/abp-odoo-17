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


class commission_config_lines(models.Model):
    _name = "commission.config.lines"
    _description = 'Sale Commission Configration Lines'
    
    from_amount = fields.Float('Start Total', required="1")
    to_amount = fields.Float('End Total', required="1")
    salesperson_per = fields.Float('Salesperson(%)')
    manager_per = fields.Float('Manager(%)')
    salesperson_amount = fields.Float('Salesperson Amount')
    manager_amount = fields.Float('Manager Amount')
    team_id = fields.Many2one('crm.team', string='Sales Team')
    categ_id = fields.Many2one('product.category', string='Product Category')
    product_id = fields.Many2one('product.template', string='Product')
    
    

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:


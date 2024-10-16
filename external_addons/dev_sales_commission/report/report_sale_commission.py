# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle 
#
##############################################################################

from odoo import models, fields, api

class report_customer_loan(models.AbstractModel): 
    _name = 'report.dev_sales_commission.report_print_sale_com_template'
    _description = "Loan Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['sale.commission'].browse(docids)
        return {
            'doc_ids': docs.ids,
            'doc_model': 'sale.commission',
            'docs': docs,
        }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

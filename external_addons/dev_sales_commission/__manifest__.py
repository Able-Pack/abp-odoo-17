# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

{
    'name': 'Sales Commission From Sales Invoice, Sale Commission to Sales Person',
    'version': '17.0.1.0',
    'sequence': 1,
    'category': 'Sales',
    'description':
        """
        This Module help to create sales commission.
        \odoo app allow From Sales Invoice, Sale Commission to Sales Person, sales order based commission,Commission based on Sales invoice, Sales Commission product margin configured, sales Commission invoice, Commission payment sales person

    """,
    'summary': 'odoo app allow From Sales Invoice, Sale Commission to Sales Person, sales order based commission,Commission based on Sales invoice, Sales Commission product margin configured, sales Commission invoice, Commission payment sales person, sale commission on payment',
    'depends': ['sale_management','account'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/res_config_settings_view.xml',
        'views/product_template.xml',
        'views/product_category_views.xml',
        'views/sales_team_views.xml',
        'views/sale_commission_views.xml',
        'views/sale_commission_line_views.xml',
        'views/sale_order_views.xml',
        'views/account_move_views.xml',
        'views/account_payment_views.xml',
        'report/sale_commission_report_views.xml',
        'report/report_header.xml',
        'report/report_print_sale_commission.xml',
        'report/report_menu.xml',
        'wizard/batch_sales_commission_views.xml',
        ],
    'demo': [],
    'test': [],
    'css': [],
    'qweb': [],
    'js': [],
    'images': ['images/main_screenshot.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    
    #author and support Details
    'author': 'DevIntelle Consulting Service Pvt.Ltd',
    'website': 'http://www.devintellecs.com',    
    'maintainer': 'DevIntelle Consulting Service Pvt.Ltd', 
    'support': 'devintelle@gmail.com',
    'price':29.0,
    'currency':'EUR',
    #'live_test_url':'https://youtu.be/A5kEBboAh_k',
    'license':'LGPL-3',
    'pre_init_hook' :'pre_init_check',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

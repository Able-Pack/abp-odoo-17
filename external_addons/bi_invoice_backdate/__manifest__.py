# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Accounting Invoice Backdate and Remarks Odoo App',
    'version': '17.0.0.1',
    'category': 'Accounting',
    'summary': 'Billing Backdate Invoice Force Date customer invoice backdate Account backdate invoice backdating force date on invoice customer invoice force date vendor bill back date vendor bill backdate invoicing backdate billing force date on Accounting backdate',
    'description' :"""
       This odoo app helps user to add backdate and remarks for multiple selected customer invoice, customer credit note, vendor bill, refund, customer and vendor payment and also pass selected backdate and remarks to journal item or journal entry for that. Also selected backdate and remarks applied to all multiple selected records.

This app allow only user with "Mass Assign Backdate(Account)" access rights only can add backdate, Also user have option to enable or disable backdate and remark feature for invoice and payments. User can also enable or disable remark and make remarks mandatory for invoice and payments. Backdate will also added to journal item or journal entry created against customer invoice, customer credit note, vendor bill, refund customer payment and vendor payments. 
    """,
    'author': 'BrowseInfo',
    'website': 'https://www.browseinfo.com',
    "price": 15,
    "currency": 'EUR',
    'depends': ['base','account'],
    'data': [
        'security/ir.model.access.csv',
        'security/mass_backdate_security.xml',
        'views/res_config_views.xml',
        'views/account_move_views.xml',
        'views/account_payment_views.xml',
        'wizard/mass_assign_backdate_views.xml',
        'wizard/mass_assign_backdate_payment_views.xml',
    ],
    'license':'OPL-1',
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'live_test_url':'https://youtu.be/2fH0NANcDYM',
    "images":['static/description/Banner.gif'],
}

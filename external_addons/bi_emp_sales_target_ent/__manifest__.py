# -- coding: utf-8 --
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Employee Sales Target and Commission - Enterprise',
    'version': '17.0.0.0',
    'category': 'Sales',
    'summary': 'Employee Target Based Commission Employee Commission based Target partner commission based on target sales commission based on target sale commission user sales commission for sales team sales commission salesperson target based commission salesman target',
    'description': """ 

        Employee Sales Target and Commission in odoo,
        Create Sales Commission and Target Group in odoo,
        Set Date in odoo,
        Manage Sales Commission in odoo,
        Payslip Include Sales Commission in odoo,
        Salary Structure for Sales Commission in odoo,
        Salary Rule for Sales Commission in odoo,
        Set Salesperson in odoo,

    """,
    'author': 'BrowseInfo',
    "price": 49,
    "currency": 'EUR',
    'website': 'https://www.browseinfo.com',
    'depends': ['base', 'sale_management', 'account', 'hr_payroll', 'documents_sign', 'hr_contract'],
    'data': [
        'security/ir.model.access.csv',
        'data/sale_commission_rule_views.xml',
        'views/hr_employee_views.xml',
        'views/hr_payslip_views.xml',
        'views/sale_commission_views.xml',
        'views/sale_order_views.xml',
    ],
    'license': 'OPL-1',
    'installable': True,
    'auto_install': False,
    'live_test_url': 'https://youtu.be/pHdh7sFSf4o',
    "images": ['static/description/Banner.gif'],
}

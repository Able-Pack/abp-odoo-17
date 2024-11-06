{
    'name': 'Able Pack Report',
    'category': '',
    'sequence': 23,
    'summary': 'Able Pack Report',
    'version': '1.0',
    'description': """
    """,
    'depends': [
        # 'sale',
        # 'abp_customer_catalogue',
        'account',
    ],
    'data': [
        'reports/product_barcode.xml',
        'reports/invoice_default.xml',
        # 'reports/sale/ir_actions_report_templates.xml',
        # 'reports/sale/ir_actions_report.xml',
    ],
    'assets': {
    },
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}

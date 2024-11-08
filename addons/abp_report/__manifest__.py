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
        'base',
        'account',
    ],
    'data': [
        'reports/report_header.xml',
        'reports/product_barcode.xml',
        'reports/invoice_default.xml',
        'reports/consignment_memo.xml',
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

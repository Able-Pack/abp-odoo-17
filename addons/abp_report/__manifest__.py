{
    'name': 'Able Pack Report',
    'category': '',
    'sequence': 23,
    'summary': 'Able Pack Report',
    'version': '1.0',
    'description': """
    """,
    'depends': [
        # Should not depends to ABP module, but its ok to depends to Odoo default module
        # 'sale',
        # 'abp_customer_catalogue',
        'base',
        'account',
        'stock',
    ],
    'data': [
        'reports/report_header.xml',
        'reports/product_barcode.xml',
        'reports/document_qrcode.xml',
        'reports/invoice_default.xml',
        'reports/consignment_memo.xml',
        
        'views/stock_picking_views.xml',
    ],
    'assets': {
    },
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}

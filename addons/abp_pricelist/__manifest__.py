{
    'name': 'Able Pack Pricelist',
    'category': '',
    'sequence': 23,
    'summary': 'Able Pack Pricelist',
    'version': '17.0',
    'description': """
    """,
    'depends': [
        'sale_management',
        'product',
        'abp_report',
    ],
    'data': [
        'views/pricelist_views.xml',
        'views/pricelist_item_views.xml',
        'views/sale_order_views.xml',
        'reports/product_barcode_action.xml',
    ],
    'assets': {
    },
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}
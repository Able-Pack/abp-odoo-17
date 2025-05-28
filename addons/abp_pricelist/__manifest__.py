{
    'name': 'Able Pack Pricelist',
    'category': '',
    'sequence': 23,
    'summary': 'Able Pack Pricelist',
    'version': '17.0',
    'author': "Victor Imannuel",
    'description': """
    """,
    'depends': [
        'sale_management',
        'product',
        'stock',
        'abp_report',
    ],
    'data': [
        'data/ir_config_parameter.xml',
        'views/pricelist_views.xml',
        'views/pricelist_item_views.xml',
        'views/sale_order_views.xml',
        'views/stock_picking_views.xml',
        'reports/product_barcode_action.xml',
    ],
    'assets': {
    },
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}
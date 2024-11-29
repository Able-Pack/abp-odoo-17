{
    'name': 'Able Pack Inventory',
    'category': '',
    'sequence': 23,
    'summary': 'Able Pack Inventory',
    'version': '17.0',
    'description': """
    """,
    'depends': [
        'product',
        'stock',
        'stock_landed_costs',
        'abp_report'
    ],
    'data': [
        'views/res_partner_views.xml',
        'views/stock_picking_views.xml',
        'views/product_views.xml',
    ],
    'assets': {
    },
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}
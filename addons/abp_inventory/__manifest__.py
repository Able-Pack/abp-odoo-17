{
    'name': 'Able Pack Inventory',
    'category': '',
    'sequence': 23,
    'summary': 'Able Pack Inventory',
    'version': '17.0',
    'description': """
    """,
    'depends': [
        'stock',
        'stock_landed_costs',
        'abp_report'
    ],
    'data': [
        'views/stock_picking_views.xml',
    ],
    'assets': {
    },
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}
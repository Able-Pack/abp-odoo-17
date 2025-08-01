{
    'name': 'Able Pack - Packing List',
    'category': '',
    'sequence': 3,
    'author': 'Victor',
    'summary': 'Able Pack - Packing List',
    'version': '17.0',
    'description': """
        A module to generate packing list PDF reports in Odoo 17.
    """,
    'depends': [
        'account',
    ],
    'data': [
        'views/account_move_views.xml',
        'reports/packing_list.xml',
    ],
    'assets': {
    },
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
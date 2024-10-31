{
    'name': 'Able Pack Salesperson Dashboard',
    'category': '',
    'sequence': 23,
    'author': 'Victor (Child of God)',
    'summary': 'Able Pack Salesperson Dashboard',
    'version': '17.0',
    'description': """
        A module that accomodate all the needs of Able Pack's salesperson
    """,
    'depends': [
        'account_reports',
        'contacts',
        'sale',
        'sales_team',
        'stock',
    ],
    'data': [
        'views/res_partner_views.xml',
        'views/menu_items.xml',
    ],
    'assets': {
    },
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
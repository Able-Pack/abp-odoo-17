{
    'name': 'Able Pack Accounting',
    'version': '17.0',
    'author': 'Victor Imannuel (Child of God)',
    'sequence': 23,
    'category': 'Able Pack',
    'summary': 'Able Pack Accounting',
    'description': """
    """,
    'depends': [
        'account',
        'abp_report',
    ],
    'data': [
        'reports/report_action.xml',
        'views/account_move_views.xml',
    ],
    'assets': {
    },
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}
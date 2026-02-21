# -*- coding: utf-8 -*-
{
    'name': 'Able Pack - Schedule Journal Entry Template',
    'version': '17.0.1.0.0',
    'sequence': 3,
    'category': 'Accounting',
    'summary': 'Schedule Journal Entry Template',
    'description': """
        This module allows users to set a schedule date on journal entry templates.
        
        Features:
        - Add a schedule date field to journal entry templates.
        - Helps in planning and automating the posting of journal entries.
    """,
    'author': 'Victor Imannuel (Child of God)',
    'website': 'https://www.ablepack.com',
    'depends': [
        'account_move_template'
    ],
    'data': [
        # Data
        'data/ir_cron.xml',

        # Views
        'views/account_move_template_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}

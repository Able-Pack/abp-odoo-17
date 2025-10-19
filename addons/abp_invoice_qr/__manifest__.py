# -*- coding: utf-8 -*-
{
    'name': 'Able Pack - Invoice QR Image',
    'version': '17.0.1.0.0',
    'sequence': 3,
    'category': 'Accounting',
    'summary': 'Add configurable QR image field to company and display on invoices',
    'description': """
        This module adds a configurable QR image field to the company (res.company) model
        and displays it on customer invoice PDFs below the company information.
        
        Features:
        - Binary field for QR image in company form
        - QR image display on invoice reports
        - Clean and configurable implementation
    """,
    'author': 'Victor Imannuel (Child of God)',
    'website': 'https://www.ablepack.com',
    'depends': ['base', 'account'],
    'data': [
        'views/res_company_views.xml',
        'reports/invoice_report.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}

# -*- coding: utf-8 -*-

{
    'name': 'Customer Account Statement and Customer Aging Reports',
    "author": "Edge Technologies",
    'version': '17.0.1.0',
    'live_test_url': "https://youtu.be/2FQEC0aYUug",
    "images":['static/description/main_screenshot.png'],
    'summary': "Customer Account Statement Customer Statement Payment followup customer accounting statement customer aging report aged customer reports print customer statement print vendor statement overdue payment report account followup payment aging partner aging",
    'description': """This app feature like print customer account statement with invoice date and due date wise and also month wise and feature for send mail to customer""",
    "license" : "OPL-1",
    'depends': ['account'],
    'data': [
            'security/ir.model.access.csv',
            'data/paperformat.xml',
            'report/report.xml',
            'data/mail_template.xml',
            'views/res_partner_inherited_view.xml',
            'wizard/customer_statement_wizard_view.xml',
            'report/customer_statement_report.xml',
            ],
    'installable': True,
    'auto_install': False,
    'price': 18,
    'currency': "EUR",
    'category': 'Accounting',

}


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

{
    'name': 'Able Pack Core Module',
    'category': '',
    'sequence': 23,
    'summary': 'Able Pack Core Module',
    'version': '1.0',
    'description': """
        To install all ablepack's dependencies
    """,
    'depends': [
        'website',
        'website_sale',
        'sale',
        'point_of_sale',
        'account_accountant',
        'hr_expense',
        'stock',
        'mrp',
        'purchase',
        'hr',
        'web_studio',
        'bi_emp_sales_target_ent',
        'partner_commission',
        
        'web',
        'contacts',
        'abp_customer_catalogue',
        'abp_pricelist',
        'abp_contact',
        'abp_sale',
        'abp_salesperson_dashboard',
        'bi_invoice_backdate',
        'muk_web_colors',
        'sttl_prevent_auto_save',
        
        'abp_security', # should be installed last to implement able pack's security (reset app menu groups)
    ],
    'data': [
    ],
    'assets': {
    },
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
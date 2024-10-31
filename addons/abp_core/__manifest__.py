{
    'name': '(Deprecated) Able Pack Core Module',
    'category': '',
    'sequence': 23,
    'summary': 'Able Pack Core Module',
    'version': '1.0',
    'description': """
        To install all ablepack's dependencies
    """,
    'depends': [
        'web',
        'website',
        'website_sale',
        'sale',
        'contacts',
        'point_of_sale',
        'account_accountant',
        'hr_expense',
        'stock',
        'mrp',
        'purchase',
        'hr',
        'web_studio',
        'partner_commission',
        
        # ablepack addons
        'abp_utils',
        'abp_payroll',
        'abp_pricelist',
        'abp_contact',
        'abp_sale',
        'abp_salesperson_dashboard',
        'abp_customer_catalogue',
        
        # external addons
        'bi_invoice_backdate',
        'bi_order_line_with_sequence_number',
        'customer_statement_aging_app',
        'dev_sales_commission',
        'muk_web_colors',
        'one2many_search_widget',
        'reset_journal_entries',
        'sttl_prevent_auto_save',
        
        # ablepack addons
        'abp_security', # should be installed last to implement able pack's security (reset app menu groups)
    ],
    'data': [
    ],
    'assets': {
    },
    'installable': False,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
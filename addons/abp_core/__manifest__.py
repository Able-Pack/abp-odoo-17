{
    'name': 'Ablepack Core Module',
    'category': '',
    'sequence': 23,
    'summary': 'Ablepack Core Module',
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
        
        'web',
        'contacts',
        'abp_product_barcode',
        'abp_customer_catalogue',
        'abp_pricelist',
        'bi_invoice_backdate',
        'muk_web_colors',
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
{
    'name': 'Ablepack Customer Catalogue',
    'category': '',
    'sequence': 23,
    'summary': 'Ablepack Customer Catalogue',
    'version': '1.0',
    'description': """
    """,
    'depends': [
        'contacts',
        'sale',
        'point_of_sale',
        'abp_product_barcode',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/customer_catalogue_views.xml',
        'views/sale_order_views.xml',
        'views/product_template_views.xml',
        'views/res_partner_views.xml',
    ],
    'assets': {
        # 'point_of_sale._assets_pos': [
        #     'abp_customer_catalogue/static/src/js/product_list.js',
        # ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}
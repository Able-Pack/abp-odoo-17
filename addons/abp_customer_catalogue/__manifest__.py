{
    'name': 'Able Pack Customer Catalogue',
    'category': '',
    'sequence': 23,
    'summary': 'Able Pack Customer Catalogue',
    'version': '1.0',
    'description': """
    """,
    'depends': [
        'base',
        'contacts',
        'sale',
        'stock',
        'point_of_sale',
    ],
    'data': [
        'security/ir.model.access.csv',
        
        'data/ir_config_parameter.xml',
        
        'views/customer_catalogue_views.xml',
        'views/sale_order_views.xml',
        'views/stock_picking_views.xml',
        'views/product_product_views.xml',
        'views/product_template_views.xml',
        'views/res_partner_views.xml',
        
        'reports/product_barcode_action.xml',
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
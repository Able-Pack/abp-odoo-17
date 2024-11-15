{
    "name": "All in one Price Lock",

    'version': "16.0",

    'category': "General",

    "summary": "This app will lock price in sale order, purchase order and product",

    'author': "INKERP",

    'website': "https://www.INKERP.com",

    "depends": ['product', 'purchase', 'sale_management', 'stock'],

    'data': [
        'security/group.xml',
        'views/sale_order_line_view.xml',
        'views/purchase_order_line_view.xml',
        'views/product_template_view.xml'
    ],

    'images': ['static/description/banner.png'],
    'license': "OPL-1",
    'installable': True,
    'application': True,
    'auto_install': False,
}

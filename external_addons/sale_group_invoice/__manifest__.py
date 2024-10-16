# Copyright 2021-2023 Sodexis
# License OPL-1 (See LICENSE file for full copyright and licensing details).

{
    "name": "Group Summary Invoice",
    "summary": """
        This module allows the user to generate a 'Group Invoice' in SO.""",
    "version": "17.0.1.0.0",
    "category": "sale",
    "website": "https://sodexis.com/",
    "author": "Sodexis",
    "license": "OPL-1",
    "installable": True,
    "images": ["images/main_screenshot.jpg"],
    "depends": ["sale", "account"],
    "data": [
        "wizard/sale_make_invoice_advance_views.xml",
    ],
    "live_test_url": "https://youtu.be/tWMTlB9XEiw",
}

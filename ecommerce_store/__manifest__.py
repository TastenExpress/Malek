# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Select Customer on Checkout',
    'category': 'Website/Website',
    'sequence': 50,
    'summary': 'Sell your products online',
    'website': 'https://www.odoo.com/app/ecommerce',
    'version': '1.1',
    'description': "",
    'depends': ['base','website_sale'],
    'data': [
        'views/shop_payment.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,

    'assets': {
        'web.assets_frontend': [
            'ecommerce_store/static/src/js/checkout_customers.js',
            'ecommerce_store/static/src/scss/custom_shop.scss',
            "ecommerce_store/static/src/css/custom.css",
        ],
    },
    'license': 'LGPL-3',
}

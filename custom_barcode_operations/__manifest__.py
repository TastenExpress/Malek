# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Custom Barcode Operations',
    'category': 'Website/Website',
    'sequence': 50,
    'summary': 'Sell your products online',
    'website': 'https://www.odoo.com/app/ecommerce',
    'version': '1.1',
    'description': "",
    'depends': ['base','website','product','stock_barcode'],
    'data': [
        'views/stock_picking_views.xml',
        'data/data.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,

    'assets': {
        'web.assets_backend': [
            'custom_barcode_operations/static/src/**/*.js',
            'custom_barcode_operations/static/src/**/*.scss',
        ],
        'web.assets_qweb': [
            'custom_barcode_operations/static/src/**/*.xml',
        ],
    },
    'license': 'LGPL-3',
}

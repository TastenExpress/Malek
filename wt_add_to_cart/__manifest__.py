# -*- coding: utf-8 -*-

{
    "name": "website add to cart",
    "version": "15.0.0.1",
    "category": "website",
    "summary": "webiste product quick add to cart ",
    "description": """
        webiste product quick add to cart with quantity without 
        redirect on checkout page.
    """,
    "author": "Warlock Technologies Pvt Ltd.",
    "website": "http://warlocktechnologies.com",
    "support": "support@warlocktechnologies.com",
    "depends": ['website', 'website_sale', 'website_sale_wishlist'],
    "data": [
        "views/template.xml",
        "views/product_description_extended.xml",
    ],

    'assets': {
        'web.assets_frontend': [
            'wt_add_to_cart/static/src/js/custom.js',
            'wt_add_to_cart/static/src/scss/custom.scss',
        ],
    },
    "images": ['images/screen_image.png'],
    "price": 30,
    "currency": "USD",
    "application": True,
    "installable": True,
    "auto_install": False,
    "license": "OPL-1",
}

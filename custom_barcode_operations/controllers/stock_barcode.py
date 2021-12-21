# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import http, _
from odoo.http import request


class StockBarcodeCustomController(http.Controller):

    @http.route('/stock_barcode/update_notes', type='json', auth='user')
    def update_notes(self, **kw):
        vals = [{'move_id':1,'notes':'dafjdfa'},{'move_id':1,'notes':'dafjdfa'}]

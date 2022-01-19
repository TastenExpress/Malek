from odoo import http, api
from odoo.http import request
from odoo import models, fields

class Product(models.Model):
    _inherit = 'res.users'
    barcode_pass = fields.Char(string='Barcode Password')

    @api.model
    def get_barcode_password(self, args):
        login_user = args['user_id']
        barcode_entered_password = args['barcode_pass']
        user = request.env(user=login_user)['res.users'].browse(login_user)
        user_pass = user.barcode_pass
        if user_pass == barcode_entered_password:
            data = bool(1)
        else:
            data = bool(0)
        return data;



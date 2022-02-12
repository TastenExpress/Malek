from odoo import http, api
from odoo.http import request
from odoo import models, fields

class Product(models.Model):
    _inherit = 'res.users'
    barcode_pass = fields.Char(string='Barcode Password')
    is_admin = fields.Boolean("Is Barcode Operations Admin?")

    @api.model
    def get_barcode_password(self, args):
        login_user = args['user_id']
        barcode_entered_password = args['barcode_pass']
        user = request.env['res.users'].search([('is_admin','=',True)])
        if not user:
            return bool(0)
        user_pass = user[0].barcode_pass
        if user_pass == barcode_entered_password:
            data = bool(1)
        else:
            data = bool(0)
        return data;



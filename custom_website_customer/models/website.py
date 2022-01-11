from odoo import models, fields

class Website(models.Model):
    _inherit = "website"

    def get_customer_types(self):
        customer_types = self.env['web.customer.type'].sudo().search([])
        print('customer_types',customer_types)
        return customer_types

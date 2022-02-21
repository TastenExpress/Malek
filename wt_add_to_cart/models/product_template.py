# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_line_ids = fields.One2many('product.template.line', 'product_id')


class ProductTemplateLine(models.Model):
    _name = 'product.template.line'
    _description = 'Product Template Line'

    product_id = fields.Many2one('product.product', string="Product", required=True)
    quantity = fields.Integer(string="Quantity")
    prod_display_name = fields.Char(string="Display Name")
    price = fields.Float(string="Price")
 
# Part of Softhealer Technologies.

from odoo import models, fields, api
import math


class ShProductTemplate(models.Model):
    _inherit = 'product.template'

    sh_increment_qty = fields.Char('Multiples of Quantity', default='1',compute='_computecase')
    multi_website_ids = fields.One2many(
        'sh.moq.multi.website', 'product_id', string="Website wise MOQ")
    multi_website_moq = fields.Boolean(
        related="company_id.multi_website_moq", string="MOQ for Multi Website?")

    def _computecase(self):
        self.sh_increment_qty = self.packaging_ids[0].qty

class MOQwebsite(models.Model):
    _name = 'sh.moq.multi.website'
    _description = 'MOQ Multi Website'

    product_id = fields.Many2one('product.template', string="Product")
    website_id = fields.Many2one('website', string="Website")
    sh_increment_qty = fields.Char('Multiples of Quantity', default='1')


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id', 'product_uom_qty')
    def onchange_pro_qty(self):
        if self:
            for rec in self:
                multi_by = int(rec.product_id.sh_increment_qty)
                if rec.product_uom_qty < multi_by:
                    rec.product_uom_qty = multi_by
                if rec.product_uom_qty > multi_by:
                    if multi_by != 0:
                        devi_value = rec.product_uom_qty/multi_by
                        ceil_value = math.ceil(devi_value)
                        rec.product_uom_qty = ceil_value * multi_by

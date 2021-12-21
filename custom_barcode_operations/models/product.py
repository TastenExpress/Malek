from odoo import api,models, fields

class Product(models.Model):
    _inherit = 'product.product'


    @api.depends('image_1920','image_512', 'image_256')
    def _compute_website_image_url(self):
        for prod in self:
            if prod.image_512:
                # image_512 is stored, image_256 is derived from it dynamically
                prod.website_image_url = self.env['website'].image_url(prod, 'image_512', size=256)
            elif prod.image_256:
                prod.website_image_url = self.env['website'].image_url(prod, 'image_256', size=256)
            elif prod.image_1920:
                prod.website_image_url = self.env['website'].image_url(prod, 'image_1920', size=256)
            else:
                prod.website_image_url = False

            print("image_url",prod.website_image_url)

    case_barcode = fields.Char('Case Product Barcode',default='1234556')
    website_image_url = fields.Char(
        string='Image URL',
        compute='_compute_website_image_url', compute_sudo=True,store=False)



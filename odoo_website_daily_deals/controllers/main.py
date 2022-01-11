# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
##############################################################################

from odoo import fields ,SUPERUSER_ID, http, tools, _
from odoo.http import request
from odoo.exceptions import UserError
from datetime import datetime
import base64


class OdooWebsiteDealsOffers(http.Controller):
    @http.route('/download_deals_catalog', type="http", auth="public", website=True, methods=['GET', 'POST'])
    def download_catalog(self, **kw):
        if request.httprequest.method == 'POST':
            product_ids=[]
            images_add=[]
            deal = request.env['website.deals.offers'].search([('id','=',int(kw['offer_id_get']))])
            for pi in deal.offers_products:
                product_ids.append(pi.product_tmpl_id.id)
                images_add.append(pi.x_studio_add_image)
            
            datas = {
                'id': 5, 'catalog_type': 'product', 'product_ids': product_ids, 'category_ids': [],
                'price': True, 'pricelist_id': (deal.id, deal.name), 'image': True,
                'image_size': 'medium', 'description': True, 'product_link': True, 'style': kw['style'],
                'int_ref': True, 'style_box': '2', 'break_page': False, 'break_page_after_products': 1,
                'on_hand': True, 'currency_id': (2, 'USD'),
                '__last_update': datetime(2021, 12, 16, 17, 43, 54, 460597),
                'display_name': 'product.catalog.wizard,5', 'create_uid': (2, 'Mitchell Admin'),
                'create_date': datetime(2021, 12, 16, 17, 43, 54, 460597),
                'write_uid': (2, 'Mitchell Admin'),'images_add':deal.offers_products,
                'write_date': datetime(2021, 12, 16, 17, 43, 54, 460597)
                    }
            html = request.env.ref('sh_product_catalog_generator.product_catalog_report_action')._render(1, data=datas)

            categ_list = []
            catalog_type = 'product'
            product_ids = request.env['product.product'].search([])
            if catalog_type == 'product':
                for product in product_ids:
                    if product.categ_id.id not in categ_list:
                        categ_list.append(product.categ_id.id)

            catalog_id = request.env['product.catalog'].sudo().create({
                'name': 'Product Catalog.pdf',
                'categories': [(6, 0, categ_list)],
            })
            b64_pdf = base64.b64encode(html[0])
            request.env['ir.attachment'].sudo().create({
                'name': 'Product Catalog.pdf',
                'type': 'binary',
                'datas': b64_pdf,
                'res_model': 'product.catalog',
                'res_id': str(catalog_id.id),
            })
            catalog_id.sudo().write({
                'store_fname': 'Product Catalog.pdf',
                'datas': b64_pdf,
            })
            cr, uid, context = request.cr, 2, request.context
            qweb_pdf = request.env.ref('sh_product_catalog_generator.product_catalog_report_action').report_action([],
                                                                                                                   data=datas)
            pdf, _ = request.env.ref('sh_product_catalog_generator.product_catalog_report_action').with_user(
                SUPERUSER_ID)._render_qweb_pdf([1], datas)
            pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', u'%s' % len(pdf))]
            return request.make_response(pdf, headers=pdfhttpheaders)

    # deals_offers Menu
    @http.route(['/deals'], type='http', auth="public", website=True)
    def deals(self, page=0, category=None, search='', **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry


        pricelist_context = dict(request.env.context)
        pricelist = False
        if not pricelist_context.get('pricelist'):
            pricelist = request.website.get_current_pricelist()
            pricelist_context['pricelist'] = pricelist.id
        else:
            pricelist = request.env['product.pricelist'].browse(pricelist_context['pricelist'])

        request.context = dict(request.context, pricelist=pricelist.id, partner=request.env.user.partner_id)
        from_currency = request.env.user.company_id.currency_id
        to_currency = pricelist.currency_id
        compute_currency = lambda price: from_currency._convert(price, to_currency, request.env.user.company_id, fields.Date.today())

        values = {
            'compute_currency': compute_currency,
            'pricelist_context':pricelist_context,
            'pricelist' : pricelist
            }
        return request.render("odoo_website_daily_deals.deals",values)



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

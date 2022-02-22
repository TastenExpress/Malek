from odoo import http
from odoo.http import request
from odoo.exceptions import UserError
from odoo import fields, http, SUPERUSER_ID, tools, _
import base64
import datetime
class DownloadCustomer(http.Controller):
    @http.route('/download_catalog',type="http",auth="public",website=True,methods=['GET', 'POST'])
    def download_catalog(self,**kw):
        if request.httprequest.method == 'POST':
            product_cats=[]
            prodcat=request.env['product.category'].search([])

            for c in prodcat:
                product_cats.append(c.id)
            pricelistobj=request.env['product.pricelist'].search([('id','=',int(kw['product_pricelist']))])
            datas = {'id': 5, 'catalog_type': 'category', 'product_ids': [], 'category_ids': product_cats, 'price': True, 'pricelist_id':(pricelistobj.id,pricelistobj.name) , 'image': True, 'image_size': 'medium', 'description': True, 'product_link': True, 'style': kw['style'], 'int_ref': True, 'style_box': '2', 'break_page': False, 'break_page_after_products': 5,'on_hand':True, 'currency_id': (2, 'USD'), '__last_update': datetime.datetime(2021, 12, 16, 17, 43, 54, 460597), 'display_name': 'product.catalog.wizard,5', 'create_uid': (2, 'Mitchell Admin'), 'create_date': datetime.datetime(2021, 12, 16, 17, 43, 54, 460597), 'write_uid': (2, 'Mitchell Admin'), 'write_date': datetime.datetime(2021, 12, 16, 17, 43, 54, 460597)}
            if kw['style']=='style_5':
                datas['break_page']=4
#             else:
#                 datas['break_page']=2
#                 datas['break_page_after_products']: False
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
            qweb_pdf= request.env.ref('sh_product_catalog_generator.product_catalog_report_action').report_action([], data=datas)
            pdf, _ = request.env.ref('sh_product_catalog_generator.product_catalog_report_action').with_user(SUPERUSER_ID)._render_qweb_pdf([1],datas)
            pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', u'%s' % len(pdf))]
            return request.make_response(pdf, headers=pdfhttpheaders)
        else:
            pricelist = http.request.env['product.pricelist'].sudo().search([])
            return http.request.render('sh_product_catalog_generator.website_catalog_down',{'pricelist':pricelist})

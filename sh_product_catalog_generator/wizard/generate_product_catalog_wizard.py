# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields, api
from odoo.exceptions import UserError
import base64
import datetime

class ProductCatalogReport(models.AbstractModel):
    _name = 'report.sh_product_catalog_generator.product_catalog_doc'
    _description = "product catalog report abstract model"

    @api.model
    def _get_report_values(self, docids, data=None):
        product_obj = self.env["product.product"]
        final_product_dic = {}
        product_dict_list = []
        row_list = []
        count = 0
        currency_id = self.env['res.currency'].sudo().browse(
            data.get('currency_id')[0])
        if data.get('catalog_type') == 'product':
            if data.get('product_ids'):
                total_product = len(data.get('product_ids'))
                for product in data.get('product_ids'):
                    domain = [("id", "=", product)]
                    search_products = product_obj.search(domain)
                    
                    if search_products:
                        price = 0.0
                        case_qty=""
                        if data.get('pricelist_id'):
                            pricelist_id = self.env['product.pricelist'].sudo().browse(
                                data.get('pricelist_id')[0])
                            price = pricelist_id._compute_price_rule([(search_products, 1.0, self.env.user.partner_id.id)], date=fields.Date.today(
                            ), uom_id=search_products.uom_id.id)[search_products.id][0]
                        
                        else:
                            if search_products.product_tmpl_id.packaging_ids:
                                for pid in search_products.product_tmpl_id.packaging_ids:
                                    case_qty=str(search_products.qty_available/pid.qty)
                                    break
                            price = search_products.list_price
                        product_dic = {
                            'id': search_products.id,
                            'default_code': search_products.default_code,
                            'name': search_products.name,
                            'cat_name': search_products.categ_id.name,
                            'image': search_products.image_1920,
                            'price': price,
                            'description': search_products.description_sale,
                            'template_id': search_products.product_tmpl_id.id,
                            'currency_id': currency_id.symbol,
                            'qty_available2': search_products.qty_available,
                            'upc': search_products.product_tmpl_id.upc,
                            'expiry':search_products.product_tmpl_id.expiry_lot_date,
                            'min_order_qty':search_products.product_tmpl_id.min_qty,
                            'case':case_qty,
                            "label":search_products.product_tmpl_id.bilingual_frenchlabel

                        }
                        product_dict_list.append(product_dic)
                        count = count + 1
                        total_product = total_product - 1
                        if data.get('style') == 'style_2' or data.get('style') == 'style_5':
                            if int(data.get('style_box')) == 2:
                                if count == 2 or total_product == 0:
                                    count = 0
                                    row_list.append(product_dict_list)
                                    product_dict_list = []
                            elif int(data.get('style_box')) == 3:
                                if count == 3 or total_product == 0:
                                    count = 0
                                    row_list.append(product_dict_list)
                                    product_dict_list = []
                            if int(data.get('style_box')) == 4:
                                if count == 4 or total_product == 0:
                                    count = 0
                                    row_list.append(product_dict_list)
                                    product_dict_list = []

                        elif data.get('style') == 'style_4':
                            if count == 2 or total_product == 0:
                                count = 0
                                row_list.append(product_dict_list)
                                product_dict_list = []
        elif data.get('catalog_type') == 'category':
            if data.get('category_ids'):
                for category in data.get('category_ids'):
                    product_list = []
                    row_list = []
                    domain = [("categ_id", "=", category)]
                    search_products = product_obj.search(domain)
                    total_product = len(search_products.ids)
                    if search_products:
                        for rec in search_products:
                            price = 0.0
                            if data.get('pricelist_id'):
                                pricelist_id = self.env['product.pricelist'].sudo().browse(
                                    data.get('pricelist_id')[0])
                                price = pricelist_id._compute_price_rule(
                                    [(rec, 1.0, self.env.user.partner_id.id)], date=fields.Date.today(), uom_id=rec.uom_id.id)[rec.id][0]
                            else:
                                price = rec.list_price

                            case_qty=""
                            if rec.product_tmpl_id.packaging_ids:
                                for pid in rec.product_tmpl_id.packaging_ids:
                                    case_qty=str(rec.qty_available/pid.qty)
                                    break
                            product_dic = {
                                'default_code': rec.default_code,
                                'name': rec.name,
                                'cat_name': rec.categ_id.name,
                                'image': rec.image_1920,
                                'price': price,
                                'description': rec.description_sale or '',
                                'template_id': rec.product_tmpl_id.id,
                                'currency_id': currency_id.symbol,
                                'id': rec.id,
                                'qty_available2': rec.qty_available,
                                'upc': rec.product_tmpl_id.upc,
                                'expiry':rec.product_tmpl_id.expiry_lot_date,
                                'min_order_qty':rec.product_tmpl_id.min_qty,
                                'case':case_qty,
                                "label":rec.product_tmpl_id.bilingual_frenchlabel
                            }
                            
                            product_list.append(product_dic)
                            count = count + 1
                            total_product = total_product - 1
                            if data.get('style') == 'style_2' or data.get('style') == 'style_5':
                                if int(data.get('style_box')) == 2:
                                    if count == 2 or total_product == 0:
                                        count = 0
                                        row_list.append(product_list)
                                        product_list = []
                                elif int(data.get('style_box')) == 3:
                                    if count == 3 or total_product == 0:
                                        count = 0
                                        row_list.append(product_list)
                                        product_list = []
                                if int(data.get('style_box')) == 4:
                                    if count == 4 or total_product == 0:
                                        count = 0
                                        row_list.append(product_list)
                                        product_list = []
                            elif data.get('style') == 'style_4':
                                if count == 2 or total_product == 0:
                                    count = 0
                                    row_list.append(product_list)
                                    product_list = []
                    search_category = self.env['product.category'].search([
                        ('id', '=', category)
                    ], limit=1)
                    if search_category and data.get('style') == 'style_2' or data.get('style') == 'style_5' or data.get('style') == 'style_4':
                        final_product_dic.update(
                            {search_category.name: row_list})
                    else:
                        final_product_dic.update(
                            {search_category.name: product_list})
        data = {
            'catalog_type': data['catalog_type'],
            'price': data['price'],
            'image': data['image'],
            'image_size': data['image_size'],
            'description': data['description'],
            'product_link': data['product_link'],
            'style': data['style'],
            'row_list': row_list,
            'int_ref': data['int_ref'],
            'on_hand': data['on_hand'],
            # 'upc': data['upc'],
            # 'expiry': data['expiry'],
            # 'min_order_qty': data['min_order_qty'],
            # 'case_pack': data['case_pack'],
            # 'bi_lang': data['bi_lang'],
            'product_dict_list': product_dict_list,
            'final_product_dic': final_product_dic,
            'style_box': data['style_box'],
            'break_page': data['break_page'],
            'break_page_after_products': data['break_page_after_products'],
        }
        return data


class GenerateProductCatalogWizard(models.TransientModel):
    _name = 'product.catalog.wizard'
    _description = 'Product Catalog Wizard'

    catalog_type = fields.Selection(
        [('product', 'Product'), ('category', 'Category')], default='product', string="Catalog Type")
    product_ids = fields.Many2many('product.product', string='Products')
    category_ids = fields.Many2many('product.category', string='Categories')
    price = fields.Boolean(string='Price')
    pricelist_id = fields.Many2one('product.pricelist', 'Pricelist')
    image = fields.Boolean(string='Image')
    image_size = fields.Selection([('small', 'Small'), ('medium', 'Medium'), (
        'large', 'Large')], default='small', string='Image Size')
    description = fields.Boolean('Description')
    on_hand = fields.Boolean('On Hand')
    product_link = fields.Boolean('Product Link')
    style = fields.Selection([('style_1', 'Style 1'), ('style_2', 'Style 2'), ('style_3', 'Style 3'), (
        'style_4', 'Style 4'), ('style_5', 'Style 5')], default='style_1', string='Style')
    int_ref = fields.Boolean('Internal Reference')
    style_box = fields.Selection([('2', '2 box per row'), ('3', '3 box per row'), (
        '4', '4 box per row')], default='2', string='Print Box Per Row')
    break_page = fields.Boolean(string='Break Page')
    break_page_after_products = fields.Integer(
        string='Break page after products', default=1)
    currency_id = fields.Many2one('res.currency', 'Currency', required=True)

    @api.onchange('style')
    def onchange_style(self):
        if self.style == 'style_2':
            self.price = True
            self.image = True
            self.int_ref = True
            self.on_hand = True
            self.product_link = True
            self.description = True
        if self.style == 'style_1':
            self.break_page = False

    @api.model
    def default_get(self, fields_list):
        res = super(GenerateProductCatalogWizard,
                    self).default_get(fields_list)
        res.update({
            'currency_id': self.env.company.currency_id.id,
        })
        return res

    @api.onchange('currency_id')
    def onchange_currency(self):
        self.pricelist_id = False
        price_list = self.env['product.pricelist'].sudo().search(
            [('currency_id', '=', self.currency_id.id)]).ids
        domain = {'pricelist_id': [('id', 'in', price_list)]}
        return {'domain': domain}

    @api.onchange('price')
    def onchange_price(self):
        if self.style == 'style_2' and not self.price:
            raise UserError('Required for style 2')

    @api.onchange('image')
    def onchange_image(self):
        if self.style == 'style_2' and not self.image:
            raise UserError('Required for style 2')

    @api.onchange('int_ref')
    def onchange_int_ref(self):
        if self.style == 'style_2' and not self.int_ref:
            raise UserError('Required for style 2')

    @api.onchange('on_hand')
    def onchange_on_hand(self):
        if self.style == 'style_2' and not self.on_hand:
            raise UserError('Required for style 2')

    @api.onchange('product_link')
    def onchange_product_link(self):
        if self.style == 'style_2' and not self.product_link:
            raise UserError('Required for style 2')

    @api.onchange('description')
    def onchange_description(self):
        if self.style == 'style_2' and not self.description:
            raise UserError('Required for style 2')

    def print_report(self):
        datas = self.read()[0]
        # raise
        html = self.env.ref('sh_product_catalog_generator.product_catalog_report_action')._render(
            self.ids, data=datas)
#         raise UserError(str(datas))
        categ_list = []
        if self.catalog_type == 'product':
            for product in self.product_ids:
                if product.categ_id.id not in categ_list:
                    categ_list.append(product.categ_id.id)
        elif self.catalog_type == 'category':
            for category in self.category_ids:
                if category.id not in categ_list:
                    categ_list.append(category.id)
        catalog_id = self.env['product.catalog'].sudo().create({
            'name': 'Product Catalog.pdf',
            'categories': [(6, 0, categ_list)],
        })
        b64_pdf = base64.b64encode(html[0])
        self.env['ir.attachment'].sudo().create({
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
        return self.env.ref('sh_product_catalog_generator.product_catalog_report_action').report_action([], data=datas)


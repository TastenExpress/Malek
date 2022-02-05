from odoo import addons
from odoo import http
from odoo.http import request



class WebsiteSaleInherit(http.Controller):

    @http.route('/getcustomers', type='json', auth='public')
    def _get_customers_json(self,**search):
        customer_dic=[]
        if 'search' in search:
            search_string = search.get('search')
            obj_partner = request.env['res.partner'].sudo()
            if search_string:

                customer = obj_partner.search(
                    [
                    ('parent_id','=',False),('create_uid','=',request.env.user.id),
                     "|",('name','ilike',search_string),
                     "|",('email','ilike',search_string),
                     "|",('phone','ilike',search_string),
                     "|",('mobile','ilike',search_string),
                     "|",('street','ilike',search_string),
                      ('street2','ilike',search_string)

                     ],order = 'name')

                manager_accountants = obj_partner.search([('parent_id','!=',False),('create_uid','=',request.env.user.id),('name', 'ilike', search_string),
                                                          "|",('function','=ilike','manager'),
                                                          ('function','=ilike','accountant'),

                                                          ],order = 'name')

                for partner_id in manager_accountants:
                    if partner_id.parent_id not in customer:
                        customer_dic.append({"id": partner_id.parent_id.id, "name": partner_id.parent_id.name+" (%s)"%partner_id.name})
                        # customer+=partner_id.parent_id
            else:
                customer = obj_partner.search([('parent_id', '=', False), ('create_uid', '=', request.env.user.id)],order = 'name')

            for rec in customer:
                customer_dic.append({"id":rec.id,"name":rec.name})

        print("customer_dic", customer_dic)
        return customer_dic

    @http.route('/update_order_customer', type='json', auth='public')
    def _update_customers_json(self,customer_id):
        if not customer_id:
            return "Invalid Customer Selection!!!"

        sale_order_id = request.session.get('sale_order_id')
        customer_dic=[]
        customer = request.env['res.partner'].sudo().browse(customer_id)
        if not customer:
            return "Invalid Customer Selection!!!"

        order = request.env['sale.order'].sudo().browse(sale_order_id)
        if not order:
            return "Order Not Found"

        try:

            partner_invoice_id = request.env['res.partner'].sudo().search(
                [('type', '=', 'invoice'), ('parent_id', '=', int(customer_id))])
            if not partner_invoice_id:
                partner_invoice_id = customer

            partner_shipping_id = request.env['res.partner'].sudo().search(
                [('type', '=', 'delivery'), ('parent_id', '=', int(customer_id))])
            if not partner_shipping_id:
                partner_shipping_id = customer

            order.sudo().write({"partner_id":int(customer.id),"partner_invoice_id":int(partner_invoice_id.id),"partner_shipping_id":int(partner_shipping_id.id)})
        except Exception as ex:
            return ex
        return "Customer Update!!!"

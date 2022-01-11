import werkzeug
from odoo import http, _
from odoo.http import request
from odoo.exceptions import UserError, _logger
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.addons.web.controllers.main import ensure_db, Home, SIGN_UP_REQUEST_PARAMS
from odoo.addons.base_setup.controllers.main import BaseSetup
from odoo.exceptions import UserError
from odoo.addons.auth_signup.controllers.main import AuthSignupHome



class WebsiteSignUpInherit(AuthSignupHome):
    @http.route(['/web/signup'],type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):

        qcontext = self.get_auth_signup_qcontext()
        print("qcontext123",qcontext)
        login_user = request.env.user.partner_id

        if not qcontext.get('token') and not qcontext.get('signup_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                self.do_signup(qcontext)
                User = request.env['res.users']
                user_sudo = User.sudo().search(
                    User._get_login_domain(qcontext.get('login')), order=User._get_login_order(), limit=1
                )
                # Send an account creation confirmation email
                if qcontext.get('token'):
                    user_sudo = User.sudo().search(
                        User._get_login_domain(qcontext.get('login')), order=User._get_login_order(), limit=1
                    )
                    template = request.env.ref('auth_signup.mail_template_user_signup_account_created', raise_if_not_found=False)
                    if user_sudo and template:
                        template.sudo().send_mail(user_sudo.id, force_send=True)

                if kw.get('customer_type'):
                    cust_type = kw['customer_type']
                    user_sudo.partner_id.Customer_Type = cust_type
                    # partner_id = user_sudo.partner_id
                    # res_partner = request.env['res.partner'].sudo().search([('id', '=', partner_id.id)])
                    # if res_partner:
                    #     res_partner.sudo().write({"Customer_Type": kw['customer_type']})
                return self.web_login(*args, **kw)
            except UserError as e:
                qcontext['error'] = e.args[0]
            except (SignupError, AssertionError) as e:
                if request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))]):
                    qcontext["error"] = _("Another user is already registered using this email address.")
                else:
                    _logger.error("%s", e)
                    qcontext['error'] = _("Could not create a new account.")

        response = request.render('auth_signup.signup', qcontext)
        response.headers['X-Frame-Options'] = 'DENY'
        return response




class CreatePatient(http.Controller):
    @http.route('/create_customer_cus',type="http",auth="user",website=True)
    def customer_form(self,**kw):
        country = http.request.env['res.country'].sudo().search([])
        login_user=request.env.user.partner_id
        return http.request.render('custom_website_customer.create_customer',{'country':country})

    @http.route('/create/customer',type='http',auth='user',website=True)
    def Customer_created(self,**kw):
        print(kw)
        login_user = request.env.user.partner_id
        main_customer={
            'company_type':'company',
            'name':kw['company_name'],
            'street':kw['company_address'],
            'city':kw['company_city'],
            'country_id':int(kw['company_country']),
            'zip':kw['company_zip'],
            'phone':kw['company_phone'],
            'mobile':kw['company_mobile'],
            'email':kw['company_email'],
            'website':kw['company_website'],
            'Customer_Type': kw['customer_type'],
            'user_id':request.env.user.id
        }
        created_main=request.env['res.partner'].sudo().create(main_customer)
        print("Main created",created_main)
        if kw['manager_name']:
            Create_manager={
                'function':'Manager',
                'parent_id':created_main.id,
                'company_type': 'person',
                'type': 'contact',
                'name':kw['manager_name'],
                'email':kw['manager_email'],
                'phone':kw['manager_phone'],
                'mobile':kw['manager_fax_no'],
                'user_id':request.env.user.id

            }
            created_manager=request.env['res.partner'].sudo().create(Create_manager)
            print("manager Created",created_manager)
        if kw['accountent_name']:
            create_accountent={
                'parent_id': created_main.id,
                'name':kw['accountent_name'],
                'function': 'Accountent',
                'type':'contact',
                'company_type': 'person',
                'email':kw['accountent_email'],
                'phone':kw['accountent_phone'],
                'mobile':kw['accountent_fax_no'],
                'user_id':request.env.user.id
            }
            created_accountent = request.env['res.partner'].sudo().create(create_accountent)
            print("Accountent Created", created_accountent)
        create_billing={
            'name':kw['billing_name'],
            'email':kw['billing_email'],
            'phone':kw['billing_phone'],
            'street':kw['billing_address'],
            'city':kw['billing_city'],
            'country_id':int(kw['billing_country']),
            'zip':kw['billing_zip'],
            'parent_id': created_main.id,
            'type': 'invoice',
            'user_id':request.env.user.id
        }
        created_billing = request.env['res.partner'].sudo().create(create_billing)
        print("Billing Created", created_billing)
        if kw['shipping_name']:
            create_shipping = {
                'name': kw['shipping_name'],
                'email': kw['shipping_email'],
                'phone': kw['shipping_phone'],
                'street': kw['shipping_address'],
                'city': kw['shipping_city'],
                'country_id': int(kw['shipping_country']),
                'zip': kw['shipping_zip'],
                'parent_id': created_main.id,
                'type': 'delivery',
                'user_id':request.env.user.id

            }
            created_shipping = request.env['res.partner'].sudo().create(create_shipping)
            print("Shipping Created", created_shipping)

        return http.request.render('custom_website_customer.customer_created_thanks',{})

odoo.define('wt_add_to_cart.custom', function (require) {
'use strict';

var core = require('web.core');
var publicWidget = require('web.public.widget');
var wSaleUtils = require('website_sale.utils');
var Dialog = require('web.Dialog');
var _t = core._t;

publicWidget.registry.WebsiteSale =  publicWidget.Widget.extend({

//publicWidget.registry.WebsiteSale.extend({
//    events: _.extend({}, options.Class.prototype.events || {}, {
    events: _.extend({}, publicWidget.Widget.prototype.events, {
        'click .add_to_cart_json_cl': 'add_to_cart_customer',
        'click .js_remove_product_item': 'remove_product_cart_qty'
    }),
    add_to_cart_customer:function(ev){
    alert(1);
        var $input = $(ev.target).closest('form').find("input[name='add_qty']");
        var $product_id = $(ev.target).closest('form').find("input[name='product_id']");
        var value = parseInt($input.val() || 0, 10);
        var add_product_id = parseInt($product_id.val(), 10);
        debugger;
        this._rpc({
            route: "/shop/cart/update_json",
            params: {
                product_id: add_product_id,
                add_qty: value,
            },
        }).then(function (data) {
            var $q = $(".my_cart_quantity");
            if (data.cart_quantity) {
                _.each($(".my_cart_quantity"), function(qn){
                    $(qn).closest('.o_wsale_my_cart').removeClass('d-none');
                    $(qn).text(data.cart_quantity);
                });
                var htmlcon = "<div id='notification_cart'>"+
                                "Your product has added successfully"+
                                "</div>"
                $("#notification_cart").remove();
                $('header').first().before(htmlcon);
                setTimeout(function(){
                    $("#notification_cart").remove();
                },2000);
                
            }
            if(data.cart_products){
                $('.cart_products_display_data').html(data.cart_products);
            }
        });
    },
    remove_product_cart_qty: function(ev){
        var self = this;
        var datas = $(ev.currentTarget).data();
        this._rpc({
            route: "/shop/cart/update_json",
            params: {
                product_id: datas.product_id,
                line_id: datas.line_id,
                set_qty: 0,
            },
        }).then(function (data) {
            var $q = $(".my_cart_quantity");
            if (data.cart_quantity) {
                _.each($(".my_cart_quantity"), function(qn){
                    $(qn).text(data.cart_quantity);
                });
            }else{
                window.location.reload()
            }
            if(data.cart_products){
                $('.cart_products_display_data').html(data.cart_products);
            }
        });
    }
});

});

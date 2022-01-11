
odoo.define('ecommerce_store.current_stock', function (require) {
'use strict';

var publicWidget = require('web.public.widget');

publicWidget.registry.portalDetails =  publicWidget.Widget.extend({
    selector: '.oe_website_sale',
    events: {
        'change #select_customer': 'onChangeCustomer',
    },
    start: function () {
        var def = this._super.apply(this, arguments);
        this.getcustomers();
        return def;
    },
    getcustomers: function (ev) {
		var self= this;

        this._rpc({
            route: "/getcustomers",
        }).then(function (data) {
        console.log('dataaaaaa',data);
            var options = "<option id=0>Select Customer</option>";
            for (let i = 0; i < data.length; i++) {
                options += "<option id="+data[i]['id']+">"+data[i]['name']+"</option>";
            }
            $('#select_customer').html(options).select2();
        });
    },

    onChangeCustomer:function(ev){
        var customer_id = $('option:selected', '#select_customer').attr('id');
        $.blockUI();

        this._rpc({
            route: "/update_order_customer",
            params: {
                customer_id: customer_id,
            },
        }).then(function (data) {
            $.unblockUI();
            alert(data);
        }).then(function(){
            $.unblockUI();
        })

    },

});

});

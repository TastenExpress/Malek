
odoo.define('ecommerce_store.current_stock', function (require) {
'use strict';

var publicWidget = require('web.public.widget');

publicWidget.registry.portalDetails =  publicWidget.Widget.extend({
    selector: '.oe_website_sale',
    events: {
        'change #select_customer': 'onChangeCustomer',
        'keyup #select_customer': 'getcustomers'
    },
    start: function () {
        var def = this._super.apply(this, arguments);
        this.getcustomers();
        return def;
    },
    getcustomers: function (ev) {
		var self= this;
        var search_string = $('#select_customer').val();
        var options = "<option>Select Customer</option>"
        this._rpc({
            route: "/getcustomers",
            params: {
                search: search_string,
            },
        }).then(function(data) {
            for (let i = 0; i < data.length; i++) {
                options += "<option data-id="+data[i]['id']+">"+data[i]['name']+"</option>";
            };
            $('#select_customers').html(options);
        });
    },

    onChangeCustomer:function(ev){

        var customer_name = $('#select_customer').val();
        var customer_id = $('#select_customers option').filter(function() {
            return this.value == customer_name;
        }).data('id');
        if(!customer_id) return;
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

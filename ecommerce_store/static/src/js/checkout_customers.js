
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
//        alert(search_string);
//        if(!search_string) return;
        this._rpc({
            route: "/getcustomers",
            params: {
                search: search_string,
            },
        }).then(function(data) {
            var data_list= "<datalist id='select_customers'>";
            //$('#select_customer').html(data);
            var options = ""
            for (let i = 0; i < data.length; i++) {
                options += "<option data-id="+data[i]['id']+">"+data[i]['name']+"</option>";
            };
            var existing_data_list = $('#select_customers').html();
            console.log("existing_data_list",existing_data_list);
            if(!existing_data_list){
                data_list+='"'+options+'"'+"</datalist>";
                $('#select_customer').append(data_list);
            }
//            else{
//                existing_data_list.html(options);
//            }
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

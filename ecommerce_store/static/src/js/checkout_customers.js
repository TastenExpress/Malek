
odoo.define('ecommerce_store.current_stock', function (require) {
'use strict';

var publicWidget = require('web.public.widget');

publicWidget.registry.portalDetails =  publicWidget.Widget.extend({
    selector: '.oe_website_sale',
    events: {
        'change #select_customer': 'onChangeCustomer',
        'keyup #select_customer': 'getcustomers',
        'click #select_customer': 'toggle_dropdown',
        'click .list_values': 'select_customer'
    },
    start: function () {
        var def = this._super.apply(this, arguments);
        this.getcustomers();
        return def;
    },
    select_customer:function(ev){

        console.log('evvvvvvv',ev);
        var id = ev.target.getAttribute('data-id');
        var name = ev.target.innerHTML;
        this.toggle_dropdown();
        $('#select_customer').attr('data-id',id);
        $('#select_customer').val(name).trigger('change');

    },
    toggle_dropdown:function(ev){
        document.getElementById("select_customers").classList.toggle("show");
    },
    getcustomers: function (ev) {
		var self= this;
        var search_string = $('#select_customer').val();
        var options ="";
        this._rpc({
            route: "/getcustomers",
            params: {
                search: search_string,
            },
        }).then(function(data) {
            for (let i = 0; i < data.length; i++) {
                options += "<a class='list_values' data-id="+data[i]['id']+">"+data[i]['name']+"</a>";
            };
            $('#select_customers').html(options);
        });
    },

    onChangeCustomer:function(ev){
        var customer_id = $('#select_customer').attr('data-id');
        alert('customer_id'+customer_id);
        /*var customer_name = $('#select_customer').val();
        var customer_id = $('#select_customers option').filter(function() {
            return this.value == customer_name;
        }).data('id');*/
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

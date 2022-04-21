odoo.define('pos_product_name.pos', function (require) {
	var screens = require('point_of_sale.screens');
    
	screens.ProductListWidget.include({
		init: function(parent, options){
			var self = this;
	        this._super(parent,options);
	        $.each(self.product_list, function(key,value){
	        	var code = value['default_code'];
	        	var name = value['display_name'];
	        	if (! name.includes(code)){
	        		value['display_name'] = "[" + code + "] " + name;
	        	};
	        });
	    }
	})

});


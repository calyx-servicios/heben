odoo.define('promotion_season_brand.init', function (require) {
"use strict";
    var models = require('point_of_sale.models');

	models.load_fields('product.product', ['product_seasons_id', 'brand_id']);
	
    models.load_models([{
        model:  'pos.promotion.season',
        fields: [],
        loaded: function(self, promo_seasons){
            self.db.set_promo_seasons_by_promo_id(promo_seasons);
        }
    },{
		model:  'pos.promotion.brand',
        fields: [],
        loaded: function(self, promo_brands){
            self.db.set_promo_brands_by_promo_id(promo_brands);
        }
	}],{
        after: 'product.product'
    });
});


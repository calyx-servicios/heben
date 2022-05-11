odoo.define('promotion_season_brand.DB', function (require) {
"use strict";
    var PosDB = require('point_of_sale.DB');

    PosDB.include({
        init: function(options){
            this._super(options);
			this.seasons_by_promo_id = {};
			this.brands_by_promo_id = {};
        },
        /**
        add promotion.season to db
        **/
        set_promo_seasons_by_promo_id: function(season_promotions){
            var self = this;
            _.each(season_promotions, function(season_promotion){
                var promo_id = season_promotion.promotion_id[0];
                self.seasons_by_promo_id[promo_id] = self.templates_by_promo_id[promo_id] || [];
                self.seasons_by_promo_id[promo_id].push(season_promotion);
            })
        },
		/**
        add promotion.brand to db
        **/
        set_promo_brands_by_promo_id: function(brand_promotions){
            var self = this;
            _.each(brand_promotions, function(brand_promotion){
                var promo_id = brand_promotion.promotion_id[0];
                self.brands_by_promo_id[promo_id] = self.templates_by_promo_id[promo_id] || [];
                self.brands_by_promo_id[promo_id].push(brand_promotion);
            })
        },
        /**
        Get all pos.promotion.season row base on promotion_id
        */
        get_promo_season_by_promo_id: function(promo_id){
            var season_promos = this.seasons_by_promo_id[promo_id] || [];
            return season_promos;
        },
		/**
        Get all pos.promotion.brand row base on promotion_id
        */
        get_promo_brand_by_promo_id: function(promo_id){
            var brand_promos = this.brands_by_promo_id[promo_id] || [];
            return brand_promos;
        }
    });
});


odoo.define('status_product.models', function (require) {
var models = require('point_of_sale.models');
var _models = models.PosModel.prototype.models;

models.load_fields('product.product', ['state']);

_models[16]['domain'] = function(self){
	var domain = ['&','&',['sale_ok','=',true],['available_in_pos','=',true],['state','!=','draft'],['state','!=','low'],'|',['company_id','=',self.config.company_id[0]],['company_id','=',false]];
	if(self.config.limit_categories&&self.config.iface_available_categ_ids.length){
		domain.unshift('&');
		domain.push(['pos_categ_id','in',self.config.iface_available_categ_ids]);
	}
	if(self.config.iface_tipproduct){
		domain.unshift(['id','=',self.config.tip_product_id[0]]);
		domain.unshift('|');
	}
	return domain;
};
});

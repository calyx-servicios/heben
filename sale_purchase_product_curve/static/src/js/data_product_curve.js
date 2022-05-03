odoo.define("sale_purchase_product_curve.add_data_product_template", function (require) {
    "use strict";

require("web.dom_ready");
var fieldRegistry = require("web.field_registry");
var core = require("web.core");
var qweb = core.qweb;
const _t = core._t;
var ajax = require("web.ajax");

function _activeTabs(){
	$("a.nav-link.active").removeClass('active');
	$("div.tab-pane.active").removeClass('active');
	$("a.nav-link[role='tab']").first().addClass('active');
	$("div.tab-pane[role='tab']").first().addClass('active');	
}

var FieldMany2ManyTags = require("web.relational_fields").FieldMany2ManyTags;
var SaleCurveMany2Many = FieldMany2ManyTags.extend({
	_onClickAddData: function () {
		var order_id = $("span[name=id]").text();
		var tables = $(".table_matrix");
		var datas = [];
		$.each(tables, function (k, v){
			var eventProps = new Object();
			var div_table = $(v);
			var table_body = div_table.find("div table tbody tr");
			eventProps['product_id'] = div_table.attr('id');
			var list_data = [];
			$.each($(table_body), function(k, v){
				var inputs = $(v).find("td div.input-group input");
				$.each(inputs, function(k, v){
					var quantity = $(v).val();
					if (quantity != 0){
						var variants = $(v).attr('ptav_ids');
						list_data.push({
							'quantity': quantity,
							'variants': variants
						});
					}
				});
			});
			eventProps['lines'] = list_data;
			datas.push(eventProps);
		});
		ajax.jsonRpc("/set_data_product_curve_sale", "call", {
			"data": datas, 'order_id': order_id
		}).then(data => {
			if (data != false){
				$("button.o_form_button_save").click();
				_activeTabs();
			}
		});
	},
	_addTag: function (data) {
		this._super.apply(this, arguments);
		var elem = $(this.$el[0]);
		var data_type = $.type(data);
		var btn_accept = $("#btn-accept").length;
		if (data_type == "object") {
			var product_id = data["id"];
			ajax.jsonRpc("/get_data_product_curve", "call", {
				id: product_id,
			}).then(data => {
				if (data != false) {
					if (btn_accept == 0){
						$(elem).after("<a id='btn-accept' class='btn btn-secondary curve_accept'>" + _t("Accept") + "</a>");
						$("#btn-accept").on("click", this._onClickAddData);
					}
					$(elem).after("<div id='" + product_id + "' class='table_matrix'></div>");
					$("#" + product_id).append(
						qweb.render("product_matrix.matrix", {
							header: data.header,
							rows: data.matrix,
						})
					);
				} else {
					alert(
						"El producto seleccionado no tiene variantes configuradas!"
					);
				};
			});
		} else {
			$.each(data, function (k, v) {
				ajax.jsonRpc("/get_data_product_curve", "call", {
					id: v["id"],
				}).then(data => {
					if (data != false) {
						if (btn_accept == 0){
							$(elem).after("<a id='btn-accept' class='btn btn-secondary'>" + _t("Accept") + "</a>");
							$("#btn-accept").on("click", this._onClickAddData);
						}
						$(elem).after("<div id='" + v["id"] + "' class='table_matrix'></div>");
						$("#" + v["id"]).append(
							qweb.render("product_matrix.matrix", {
								header: data.header,
								rows: data.matrix,
							})
						);
					} else {
						alert(
							"El producto seleccionado no tiene variantes configuradas!"
						);
					}
				});
			});
		}
	},
	_onDeleteTag: function (event) {
		var data_id = $(event.target).parent().data("id");
		$("#" + data_id).remove();
		var table_matrix = $(".table_matrix").length;
		if (table_matrix == 0) {
			$("#btn-accept").remove();
		}
		this._super.apply(this, arguments);
	},
});

var SaleTemplateCurveMany2Many = FieldMany2ManyTags.extend({
	_onClickAddData: function () {
		var order_id = $("span[name=id]").text();
		var tables = $(".table_matrix");
		var datas = [];
		$.each(tables, function (k, v){
			var eventProps = new Object();
			var div_table = $(v);
			var table_body = div_table.find("div table tbody tr");
			eventProps['product_id'] = div_table.attr('id');
			var list_data = [];
			$.each($(table_body), function(k, v){
				var inputs = $(v).find("td div.input-group input");
				$.each(inputs, function(k, v){
					var quantity = $(v).val();
					if (quantity != 0){
						var variants = $(v).attr('ptav_ids');
						list_data.push({
							'quantity': quantity,
							'variants': variants
						});
					}
				});
			});
			eventProps['lines'] = list_data;
			datas.push(eventProps);
		});
		ajax.jsonRpc("/set_data_product_curve_sale_template", "call", {
			"data": datas, 'order_id': order_id
		}).then(data => {
			if (data != false){
				$("button.o_form_button_save").click();
				_activeTabs();
			}
		});
	},
	_addTag: function (data) {
		this._super.apply(this, arguments);
		var elem = $(this.$el[0]);
		var data_type = $.type(data);
		var btn_accept = $("#btn-accept").length;
		if (data_type == "object") {
			var product_id = data["id"];
			ajax.jsonRpc("/get_data_product_curve", "call", {
				id: product_id,
			}).then(data => {
				if (data != false) {
					if (btn_accept == 0){
						$(elem).after("<a id='btn-accept' class='btn btn-secondary curve_accept'>" + _t("Accept") + "</a>");
						$("#btn-accept").on("click", this._onClickAddData);
					}
					$(elem).after("<div id='" + product_id + "' class='table_matrix'></div>");
					$("#" + product_id).append(
						qweb.render("product_matrix.matrix", {
							header: data.header,
							rows: data.matrix,
						})
					);
				} else {
					alert(
						"El producto seleccionado no tiene variantes configuradas!"
					);
				};
			});
		} else {
			$.each(data, function (k, v) {
				ajax.jsonRpc("/get_data_product_curve", "call", {
					id: v["id"],
				}).then(data => {
					if (data != false) {
						if (btn_accept == 0){
							$(elem).after("<a id='btn-accept' class='btn btn-secondary'>" + _t("Accept") + "</a>");
							$("#btn-accept").on("click", this._onClickAddData);
						}
						$(elem).after("<div id='" + v["id"] + "' class='table_matrix'></div>");
						$("#" + v["id"]).append(
							qweb.render("product_matrix.matrix", {
								header: data.header,
								rows: data.matrix,
							})
						);
					} else {
						alert(
							"El producto seleccionado no tiene variantes configuradas!"
						);
					}
				});
			});
		}
	},
	_onDeleteTag: function (event) {
		var data_id = $(event.target).parent().data("id");
		$("#" + data_id).remove();
		var table_matrix = $(".table_matrix").length;
		if (table_matrix == 0) {
			$("#btn-accept").remove();
		}
		this._super.apply(this, arguments);
	},
});

var PurchaseCurveMany2Many = FieldMany2ManyTags.extend({
	_onClickAddData: function () {
		var order_id = $("span[name=id]").text();
		var tables = $(".table_matrix");
		var datas = [];
		$.each(tables, function (k, v){
			var eventProps = new Object();
			var div_table = $(v);
			var table_body = div_table.find("div table tbody tr");
			eventProps['product_id'] = div_table.attr('id');
			var list_data = [];
			$.each($(table_body), function(k, v){
				var inputs = $(v).find("td div.input-group input");
				$.each(inputs, function(k, v){
					var quantity = $(v).val();
					if (quantity != 0){
						var variants = $(v).attr('ptav_ids');
						list_data.push({
							'quantity': quantity,
							'variants': variants
						});
					}
				});
			});
			eventProps['lines'] = list_data;
			datas.push(eventProps);
		});
		ajax.jsonRpc("/set_data_product_curve_purchase", "call", {
			"data": datas, 'order_id': order_id
		}).then(data => {
			if (data != false){
				$("button.o_form_button_save").click();
				_activeTabs();
			}
		});
	},
	_addTag: function (data) {
		this._super.apply(this, arguments);
		var elem = $(this.$el[0]);
		var data_type = $.type(data);
		var btn_accept = $("#btn-accept").length;
		if (data_type == "object") {
			var product_id = data["id"];
			ajax.jsonRpc("/get_data_product_curve", "call", {
				id: product_id,
			}).then(data => {
				if (data != false) {
					if (btn_accept == 0){
						$(elem).after("<a id='btn-accept' class='btn btn-secondary curve_accept'>" + _t("Accept") + "</a>");
						$("#btn-accept").on("click", this._onClickAddData);
					}
					$(elem).after("<div id='" + product_id + "' class='table_matrix'></div>");
					$("#" + product_id).append(
						qweb.render("product_matrix.matrix", {
							header: data.header,
							rows: data.matrix,
						})
					);
				} else {
					alert(
						"El producto seleccionado no tiene variantes configuradas!"
					);
				};
			});
		} else {
			$.each(data, function (k, v) {
				ajax.jsonRpc("/get_data_product_curve", "call", {
					id: v["id"],
				}).then(data => {
					if (data != false) {
						if (btn_accept == 0){
							$(elem).after("<a id='btn-accept' class='btn btn-secondary'>" + _t("Accept") + "</a>");
							$("#btn-accept").on("click", this._onClickAddData);
						}
						$(elem).after("<div id='" + v["id"] + "' class='table_matrix'></div>");
						$("#" + v["id"]).append(
							qweb.render("product_matrix.matrix", {
								header: data.header,
								rows: data.matrix,
							})
						);
					} else {
						alert(
							"El producto seleccionado no tiene variantes configuradas!"
						);
					}
				});
			});
		}
	},
	_onDeleteTag: function (event) {
		var data_id = $(event.target).parent().data("id");
		$("#" + data_id).remove();
		var table_matrix = $(".table_matrix").length;
		if (table_matrix == 0) {
			$("#btn-accept").remove();
		}
		this._super.apply(this, arguments);
	},
});

var PurchaseRequisitionCurveMany2Many = FieldMany2ManyTags.extend({
	_onClickAddData: function () {
		var order_id = $("span[name=id]").text();
		var tables = $(".table_matrix");
		var datas = [];
		$.each(tables, function (k, v){
			var eventProps = new Object();
			var div_table = $(v);
			var table_body = div_table.find("div table tbody tr");
			eventProps['product_id'] = div_table.attr('id');
			var list_data = [];
			$.each($(table_body), function(k, v){
				var inputs = $(v).find("td div.input-group input");
				$.each(inputs, function(k, v){
					var quantity = $(v).val();
					if (quantity != 0){
						var variants = $(v).attr('ptav_ids');
						list_data.push({
							'quantity': quantity,
							'variants': variants
						});
					}
				});
			});
			eventProps['lines'] = list_data;
			datas.push(eventProps);
		});
		ajax.jsonRpc("/set_data_product_curve_prequisition", "call", {
			"data": datas, 'order_id': order_id
		}).then(data => {
			if (data != false){
				$("button.o_form_button_save").click();
				_activeTabs();
			}
		});
	},
	_addTag: function (data) {
		this._super.apply(this, arguments);
		var elem = $(this.$el[0]);
		var data_type = $.type(data);
		var btn_accept = $("#btn-accept").length;
		if (data_type == "object") {
			var product_id = data["id"];
			ajax.jsonRpc("/get_data_product_curve", "call", {
				id: product_id,
			}).then(data => {
				if (data != false) {
					if (btn_accept == 0){
						$(elem).after("<a id='btn-accept' class='btn btn-secondary curve_accept'>" + _t("Accept") + "</a>");
						$("#btn-accept").on("click", this._onClickAddData);
					}
					$(elem).after("<div id='" + product_id + "' class='table_matrix'></div>");
					$("#" + product_id).append(
						qweb.render("product_matrix.matrix", {
							header: data.header,
							rows: data.matrix,
						})
					);
				} else {
					alert(
						"El producto seleccionado no tiene variantes configuradas!"
					);
				};
			});
		} else {
			$.each(data, function (k, v) {
				ajax.jsonRpc("/get_data_product_curve", "call", {
					id: v["id"],
				}).then(data => {
					if (data != false) {
						if (btn_accept == 0){
							$(elem).after("<a id='btn-accept' class='btn btn-secondary'>" + _t("Accept") + "</a>");
							$("#btn-accept").on("click", this._onClickAddData);
						}
						$(elem).after("<div id='" + v["id"] + "' class='table_matrix'></div>");
						$("#" + v["id"]).append(
							qweb.render("product_matrix.matrix", {
								header: data.header,
								rows: data.matrix,
							})
						);
					} else {
						alert(
							"El producto seleccionado no tiene variantes configuradas!"
						);
					}
				});
			});
		}
	},
	_onDeleteTag: function (event) {
		var data_id = $(event.target).parent().data("id");
		$("#" + data_id).remove();
		var table_matrix = $(".table_matrix").length;
		if (table_matrix == 0) {
			$("#btn-accept").remove();
		}
		this._super.apply(this, arguments);
	},
});

fieldRegistry.add("sale_curve_many2many", SaleCurveMany2Many);
fieldRegistry.add("sale_template_curve_many2many", SaleTemplateCurveMany2Many);
fieldRegistry.add("purchase_curve_many2many", PurchaseCurveMany2Many);
fieldRegistry.add("p_requisition_curve_many2many", PurchaseRequisitionCurveMany2Many);
});


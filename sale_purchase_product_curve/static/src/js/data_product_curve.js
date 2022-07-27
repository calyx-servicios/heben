odoo.define("sale_purchase_product_curve.add_data_product_template", function (require) {
    "use strict";

require("web.dom_ready");
let fieldRegistry = require("web.field_registry");
let core = require("web.core");
let qweb = core.qweb;
const _t = core._t;
let ajax = require("web.ajax");

function _activeTabs(){
	$("a.nav-link.active").removeClass('active');
	$("div.tab-pane.active").removeClass('active');
	$("a.nav-link[role='tab']").first().addClass('active');
	$("div.tab-pane[role='tab']").first().addClass('active');	
}

let FieldMany2ManyTags = require("web.relational_fields").FieldMany2ManyTags;
let SaleCurveMany2Many = FieldMany2ManyTags.extend({
	_onClickAddData: function () {
		let order_id = $("span[name=id]").text();
		let tables = $(".table_matrix");
		let datas = [];
		$.each(tables, function (k, v){
			let eventProps = new Object();
			let div_table = $(v);
			let table_body = div_table.find("div table tbody tr");
			eventProps['product_id'] = div_table.attr('id');
			let list_data = [];
			$.each($(table_body), function(k, v){
				let inputs = $(v).find("td div.input-group input");
				$.each(inputs, function(k, v){
					let quantity = $(v).val();
					if (quantity != 0){
						let variants = $(v).attr('ptav_ids');
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
		let elem = $(this.$el[0]);
		let data_type = $.type(data);
		let btn_accept = $("#btn-accept").length;
		if (data_type == "object") {
			let product_id = data["id"];
			ajax.jsonRpc("/get_data_product_curve", "call", {
				id: product_id, model: "sale_order"
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
						_t("The selected product has no configured variants!")
					);
				};
			});
		} else {
			let count_accept = 0;
			let widget = this;
			$.each(data, function (k, v) {
				ajax.jsonRpc("/get_data_product_curve", "call", {
					id: v["id"], model: "sale_order"
				}).then(data => {
					if (data != false) {
						if (btn_accept == 0 && count_accept == 0){
							$(elem).after("<a id='btn-accept' class='btn btn-secondary curve_accept'>" + _t("Accept") + "</a>");
							$("#btn-accept").on("click", widget._onClickAddData);
							count_accept +=1;
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
							_t("The selected product has no configured variants!")
						);
					}
				});
			});
		}
	},
	_onDeleteTag: function (event) {
		let data_id = $(event.target).parent().data("id");
		$("#" + data_id).remove();
		let table_matrix = $(".table_matrix").length;
		if (table_matrix == 0) {
			$("#btn-accept").remove();
		}
		this._super.apply(this, arguments);
	},
});

let SaleTemplateCurveMany2Many = FieldMany2ManyTags.extend({
	_onClickAddData: function () {
		let order_id = $("span[name=id]").text();
		let tables = $(".table_matrix");
		let datas = [];
		$.each(tables, function (k, v){
			let eventProps = new Object();
			let div_table = $(v);
			let table_body = div_table.find("div table tbody tr");
			eventProps['product_id'] = div_table.attr('id');
			let list_data = [];
			$.each($(table_body), function(k, v){
				let inputs = $(v).find("td div.input-group input");
				$.each(inputs, function(k, v){
					let quantity = $(v).val();
					if (quantity != 0){
						let variants = $(v).attr('ptav_ids');
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
		let elem = $(this.$el[0]);
		let data_type = $.type(data);
		let btn_accept = $("#btn-accept").length;
		if (data_type == "object") {
			let product_id = data["id"];
			ajax.jsonRpc("/get_data_product_curve", "call", {
				id: product_id, model: "sale_order"
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
						_t("The selected product has no configured variants!")
					);
				};
			});
		} else {
			let count_accept = 0;
			let widget = this;
			$.each(data, function (k, v) {
				ajax.jsonRpc("/get_data_product_curve", "call", {
					id: v["id"], model: "sale_order"
				}).then(data => {
					if (data != false) {
						if (btn_accept == 0 && count_accept == 0){
							$(elem).after("<a id='btn-accept' class='btn btn-secondary curve_accept'>" + _t("Accept") + "</a>");
							$("#btn-accept").on("click", widget._onClickAddData);
							count_accept +=1;
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
							_t("The selected product has no configured variants!")
						);
					}
				});
			});
		}
	},
	_onDeleteTag: function (event) {
		let data_id = $(event.target).parent().data("id");
		$("#" + data_id).remove();
		let table_matrix = $(".table_matrix").length;
		if (table_matrix == 0) {
			$("#btn-accept").remove();
		}
		this._super.apply(this, arguments);
	},
});

let PurchaseCurveMany2Many = FieldMany2ManyTags.extend({
	_onClickAddData: function () {
		let order_id = $("span[name=id]").text();
		let tables = $(".table_matrix");
		let datas = [];
		$.each(tables, function (k, v){
			let eventProps = new Object();
			let div_table = $(v);
			let table_body = div_table.find("div table tbody tr");
			eventProps['product_id'] = div_table.attr('id');
			let list_data = [];
			$.each($(table_body), function(k, v){
				let inputs = $(v).find("td div.input-group input");
				$.each(inputs, function(k, v){
					let quantity = $(v).val();
					if (quantity != 0){
						let variants = $(v).attr('ptav_ids');
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
		let elem = $(this.$el[0]);
		let data_type = $.type(data);
		let btn_accept = $("#btn-accept").length;
		if (data_type == "object") {
			let product_id = data["id"];
			ajax.jsonRpc("/get_data_product_curve", "call", {
				id: product_id, model: "purchase_order"
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
						_t("The selected product has no configured variants!")
					);
				};
			});
		} else {
			let count_accept = 0;
			let widget = this;
			$.each(data, function (k, v) {
				ajax.jsonRpc("/get_data_product_curve", "call", {
					id: v["id"], model: "purchase_order"
				}).then(data => {
					if (data != false) {
						if (btn_accept == 0 && count_accept == 0){
							$(elem).after("<a id='btn-accept' class='btn btn-secondary curve_accept'>" + _t("Accept") + "</a>");
							$("#btn-accept").on("click", widget._onClickAddData);
							count_accept +=1;
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
							_t("The selected product has no configured variants!")
						);
					}
				});
			});
		}
	},
	_onDeleteTag: function (event) {
		let data_id = $(event.target).parent().data("id");
		$("#" + data_id).remove();
		let table_matrix = $(".table_matrix").length;
		if (table_matrix == 0) {
			$("#btn-accept").remove();
		}
		this._super.apply(this, arguments);
	},
});

let PurchaseRequisitionCurveMany2Many = FieldMany2ManyTags.extend({
	_onClickAddData: function () {
		let order_id = $("span[name=id]").text();
		let tables = $(".table_matrix");
		let datas = [];
		$.each(tables, function (k, v){
			let eventProps = new Object();
			let div_table = $(v);
			let table_body = div_table.find("div table tbody tr");
			eventProps['product_id'] = div_table.attr('id');
			let list_data = [];
			$.each($(table_body), function(k, v){
				let inputs = $(v).find("td div.input-group input");
				$.each(inputs, function(k, v){
					let quantity = $(v).val();
					if (quantity != 0){
						let variants = $(v).attr('ptav_ids');
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
		let elem = $(this.$el[0]);
		let data_type = $.type(data);
		let btn_accept = $("#btn-accept").length;
		if (data_type == "object") {
			let product_id = data["id"];
			ajax.jsonRpc("/get_data_product_curve", "call", {
				id: product_id, model: "purchase_order"
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
						_t("The selected product has no configured variants!")
					);
				};
			});
		} else {
			let count_accept = 0;
			let widget = this;
			$.each(data, function (k, v) {
				ajax.jsonRpc("/get_data_product_curve", "call", {
					id: v["id"], model: "purchase_order"
				}).then(data => {
					if (data != false) {
						if (btn_accept == 0 && count_accept == 0){
							$(elem).after("<a id='btn-accept' class='btn btn-secondary curve_accept'>" + _t("Accept") + "</a>");
							$("#btn-accept").on("click", widget._onClickAddData);
							count_accept +=1;
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
							_t("The selected product has no configured variants!")
						);
					}
				});
			});
		}
	},
	_onDeleteTag: function (event) {
		let data_id = $(event.target).parent().data("id");
		$("#" + data_id).remove();
		let table_matrix = $(".table_matrix").length;
		if (table_matrix == 0) {
			$("#btn-accept").remove();
		}
		this._super.apply(this, arguments);
	},
});

let StockCurveMany2Many = FieldMany2ManyTags.extend({
	_onClickAddData: function () {
		let order_id = $("span[name=id]").first().text();
		let tables = $(".table_matrix");
		let datas = [];
		$.each(tables, function (k, v){
			let eventProps = new Object();
			let div_table = $(v);
			let table_body = div_table.find("div table tbody tr");
			eventProps['product_id'] = div_table.attr('id');
			let list_data = [];
			$.each($(table_body), function(k, v){
				let inputs = $(v).find("td div.input-group input");
				$.each(inputs, function(k, v){
					let quantity = $(v).val();
					if (quantity != 0){
						let variants = $(v).attr('ptav_ids');
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
		ajax.jsonRpc("/set_data_product_curve_stock_move", "call", {
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
		let elem = $(this.$el[0]);
		let data_type = $.type(data);
		let btn_accept = $("#btn-accept").length;
		if (data_type == "object") {
			let product_id = data["id"];
			ajax.jsonRpc("/get_data_product_curve", "call", {
				id: product_id, model: "stock_move"
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
						_t("The selected product has no configured variants!")
					);
				};
			});
		} else {
			let count_accept = 0;
			let widget = this;
			$.each(data, function (k, v) {
				ajax.jsonRpc("/get_data_product_curve", "call", {
					id: v["id"],
				}).then(data => {
					if (data != false) {
						if (btn_accept == 0 && count_accept == 0){
							$(elem).after("<a id='btn-accept' class='btn btn-secondary curve_accept'>" + _t("Accept") + "</a>");
							$("#btn-accept").on("click", widget._onClickAddData);
							count_accept +=1;
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
							_t("The selected product has no configured variants!")
						);
					}
				});
			});
		}
	},
	_onDeleteTag: function (event) {
		let data_id = $(event.target).parent().data("id");
		$("#" + data_id).remove();
		let table_matrix = $(".table_matrix").length;
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
fieldRegistry.add("picking_curve_many2many", StockCurveMany2Many);
});


odoo.define(
  "sale_purchase_product_curve.add_data_product_template",
  function (require) {
    "use strict";

    require("web.dom_ready");
    var fieldRegistry = require("web.field_registry");
  //  var Widget = require('web.Widget');
  //  var publicWidget = require('web.public.widget');
    var core = require("web.core");
    var qweb = core.qweb;
    var ajax = require("web.ajax");

    var FieldMany2ManyTags =
      require("web.relational_fields").FieldMany2ManyTags;
    var CurveMany2Many = FieldMany2ManyTags.extend({
      _addTag: function (data) {
        this._super.apply(this, arguments);

        var elem = $(this.$el[0]);
        var data_type = $.type(data);
        if (data_type == "object") {
          var product_id = data["id"];
          ajax
            .jsonRpc("/get_data_product_curve", "call", {
              id: product_id,
            })
            .then((data) => {
              if (data != false) {
                $(elem).after("<div id='" + product_id + "'></div>");
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
              }
            });
        } else {
          $.each(data, function (k, v) {
            ajax
              .jsonRpc("/get_data_product_curve", "call", {
                id: v["id"],
              })
              .then((data) => {
                if (data != false) {
                  $(elem).after("<div id='" + v["id"] + "'></div>");
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
        this._super.apply(this, arguments);
      },
    });

    //var WidgetSaveData = Widget.extend({
//	    selector: ".js_class_save_data",
//	    events: {
//	      "click ": "_onClickAddData",
//	    },
//	    _onClickAddData: function (ev) {
//	      console.log("***********");
//	    }
//    });
	
    fieldRegistry.add("curve_many2many", CurveMany2Many);
 });


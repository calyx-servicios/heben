from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = "product.product"

    product_color = fields.Many2one(
        string="Color",
        comodel_name="product.template.attribute.value",
        compute="_compute_product_color",
        store=True,
    )

    product_name_and_color = fields.Char(
        string="Product Name and Color",
        compute="_compute_product_name_and_color",
        store=True,
        index=True,
    )

    def _compute_product_name_and_color(self):
        for product in self:
            product.product_name_and_color = (
                f"{product.name} - {product.product_color.name}"
            ) if product.product_color else False

    qty_available = fields.Float(
        "Quantity On Hand",
        compute="_compute_quantities",
        search="_search_qty_available",
        digits="Product Unit of Measure",
        compute_sudo=False,
        store=True,
        help="Current quantity of products.\n"
        "In a context with a single Stock Location, this includes "
        "goods stored at this Location, or any of its children.\n"
        "In a context with a single Warehouse, this includes "
        "goods stored in the Stock Location of this Warehouse, or any "
        "of its children.\n"
        "stored in the Stock Location of the Warehouse of this Shop, "
        "or any of its children.\n"
        "Otherwise, this includes goods stored in any Stock Location "
        "with 'internal' type.",
    )

    # @api.multi
    @api.depends("product_template_attribute_value_ids")
    def _compute_product_color(self):
        for product in self:
            if not product.product_template_attribute_value_ids:
                product.product_color = False
                continue
            product.product_color = product._get_product_color()
        return True

    def _get_product_color(self) -> int:
        attributes = self.product_template_attribute_value_ids
        for attribute in attributes:
            if attribute.attribute_id.name == "Color":
                return attribute.id
        return False

    def product_read(self):
        # fields = [
        #     "id",
        #     "product_template_attribute_value_ids",
        #     "attribute_line_ids",
        #     "valid_product_template_attribute_line_ids",
        # ]
        # reading = self.read(fields)
        # attribute_values = self.env["product.template.attribute.value"].browse(
        #     reading[0]["product_template_attribute_value_ids"]
        # )

        # ----------------------------------------------------------------------
        groups = self.env["product.product"].read_group(
            domain=[],
            fields=[
                "name",
                "product_color",
                "qty_available",
                "sales_count",
                "property_stock_inventory",
                "warehouse_id",
            ],
            groupby="product_color",
            lazy=True,
            limit=2,
        )
        for group in groups:
            domain = group["__domain"]
            self._compute_product_rotation(domain)

            _logger.info(group)

        return True

    def _compute_product_rotation(self, domain: list) -> dict:
        products = self.search(domain)
        fields = [
            "name",
            "product_color",
            "qty_available",
            "sales_count",
            "property_stock_inventory",
            "warehouse_id",
        ]
        grouped_values = {
            "name": products[0].name,
            "color": products[0].product_color.name,
            "qty_available": sum(products.mapped("qty_available")),
            "sales_count": sum(products.mapped("sales_count")),
        }
        _logger.info(grouped_values)
        # for product in products:
        #     _logger.info(product.read(fields))
        stock_fields = ["location_id", "product_id.product_color", "quantity"]
        stock_quants = self.env["stock.quant"].read_group(
            [("product_id", "in", products.ids)], stock_fields, ["location_id"]
        )
        # stock_quants = stock_quants.read_group(
        _logger.info(stock_quants)
        # TODO: crear transient model que se llene con los valores de product_rotation
        # TODO: poder diferenciar entre locaciones de stock
        # TODO: crear reporte que muestre los valores de product_rotation

        possible_query = """
            SELECT pp.product_color,
                COALESCE(SUM(CASE
                    WHEN sl.name = 'Customers'
                    THEN sq.quantity
                    END
                ),0) as vendidos,
                COALESCE(SUM(CASE
                    WHEN sl.name != 'Customers'
                    THEN sq.quantity
                    END
                ),0) as disponibles
            FROM product_product pp
            INNER JOIN stock_quant sq ON pp.id = sq.product_id
            INNER JOIN stock_location sl ON sq.location_id = sl.id
            GROUP BY pp.product_color
            ORDER BY pp.product_color
            LIMIT 100;
        """

        sml_query = """
        SELECT pp.product_color,
            sl.name,
            COALESCE(SUM(CASE
                    WHEN sl.name = 'Customers'
                    THEN sml.qty_done
                    END
                ),0) as vendidos,
                COALESCE(SUM(CASE
                    WHEN sl.name != 'Customers'
                    THEN sml.qty_done
                    END
                ),0) as disponibles
        FROM stock_move_line sml
        INNER JOIN stock_move sm ON sml.move_id = sm.id
        INNER JOIN product_product pp ON sml.product_id = pp.id
        INNER JOIN stock_location sl ON sml.location_dest_id = sl.id
        WHERE sml.company_id = 1
        GROUP BY pp.product_color,sl.name
        ORDER BY pp.product_color
        ;
        """
        # WHERE sl.company_id = 2 OR sl.company_id = 0

        #         , sq.location_id, sl.name
        #         sq.location_id,
        #         sl.name,

    def action_view_product_rotation(self):
        action = {
            "name": _("Product Rotation"),
            "type": "ir.actions.act_window",
            "view_mode": "pivot,tree,form",
            "res_model": "product.product",
            # 'domain': [('id', 'in', self.ids)],
            "target": "current",
            "context": {"group_by": "product_color"},
        }
        domain = []
        action["domain"] = domain
        return action

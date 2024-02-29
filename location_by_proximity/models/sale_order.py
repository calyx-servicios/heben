from odoo import fields, models
import re


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def check_location(self):
        if self.partner_shipping_id:
            client_zip = int(self.partner_shipping_id.zip)
        else:
            client_zip = int(self.partner_id.zip)
        matched_locations = self.env["stock.location"].search_by_zip(client_zip)

        locations = matched_locations + \
            matched_locations.mapped("secondary_location_ids")
        order_lines = self.order_line.filtered(
            lambda line: line.product_id.type != "service")

        for order_line in order_lines:
            house_empty = True
            for location in locations:
                stock_qty = self.env["stock.quant"].search(
                    [("product_id", "=", order_line.product_id.id),
                     ("location_id", "=", location.id)]
                ).quantity
                if order_line.product_uom_qty <= stock_qty:
                    order_line.location_id = location.id
                    house_empty = False
                    break

            if house_empty:
                msg = "For the product " + order_line.name + \
                    " there is no stock in the selected locations"
                self.message_post(body=msg)

    def action_confirm(self):
        lines_product = self.order_line.filtered(
            lambda x: x.product_id.type != 'service')
        if lines_product:
            lines_unlocated = lines_product.filtered(lambda l: not l.location_id)
            if lines_unlocated:
                order_id = lines_unlocated.mapped("order_id")
                if not order_id.partner_id.zip:
                    for line in lines_unlocated:
                        line.location_id = order_id.warehouse_id.lot_stock_id.id
                else:
                    order_id.check_location()
        if not self.user_id:
            self.user_id = self.env.user.id
        return super(SaleOrder, self).action_confirm()


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    _order = "id desc"

    location_id = fields.Many2one('stock.location')

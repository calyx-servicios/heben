from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = "sale.order.line"

    location_id = fields.Many2one(
        comodel_name="stock.location",
        string="Stock Location",
        compute="_compute_location_id",
        store=True,
    )

    @api.depends("order_id.picking_ids")
    def _compute_location_id(self):
        for line in self:
            if line.order_id.picking_ids:
                line.location_id = line.order_id.picking_ids[0].location_id.id
            else:
                line.location_id = False

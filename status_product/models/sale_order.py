from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_id = fields.Many2one('product.product')


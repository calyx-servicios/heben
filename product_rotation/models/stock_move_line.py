from odoo import models, fields, api, _

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    product_color = fields.Many2one(
        string="Color",
        related="product_id.product_color",
        store=True,
    )

    product_name_and_color = fields.Char(string="Product Name and Color", related="product_id.product_name_and_color", store=True)

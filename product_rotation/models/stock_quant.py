from odoo import models,fields

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    product_name_and_color = fields.Char(string="Product Name and Color", related="product_id.product_name_and_color", store=True)
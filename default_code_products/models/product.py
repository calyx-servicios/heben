from odoo import fields, models

class ProductProduct(models.Model):
    _inherit = "product.product"

    modelo_articulo = fields.Char('Modelo Artículo')


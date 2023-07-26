from odoo import models,fields

class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    display_type = fields.Selection(selection_add=[('size','Size')])

class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'

    code = fields.Char()
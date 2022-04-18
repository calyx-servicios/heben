from odoo import models,fields,api,_

class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'

    code = fields.Char(string ='Code')
from odoo import api, models
from .utils.barcode import generate_ean

class Product(models.Model):
    _inherit = 'product.product'

    @api.model
    def create(self, vals):
        res = super(Product, self).create(vals)
        settings = self.env['res.config.settings'].product_barcode_get_settings()
        ean = generate_ean(str(res.id), settings)
        res.barcode = ean
        return res

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def create(self, vals_list):
        templates = super(ProductTemplate, self).create(vals_list)
        settings = self.env['res.config.settings'].product_barcode_get_settings()
        ean = generate_ean(str(templates.id), settings)
        templates.barcode = ean
        return templates

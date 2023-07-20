from odoo import fields, models

class GtMagentoStore(models.Model):
    _inherit = "gt.magento.store"

    stock_location_ids = fields.Many2many('stock.location',string='Location')


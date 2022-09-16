from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class StockLocation(models.Model):
    _inherit = 'stock.location'
    _order = 'sequence'

    name = fields.Char(required=False)
    contact = fields.Many2one('res.partner')
    zip_code_field = fields.Char("Postal Code")
    from_zip = fields.Integer()
    to_zip = fields.Integer()
    zip_code = fields.Integer("Zip")
    location_id = fields.Many2one('stock.location')
    secondary_location_ids = fields.Many2many('stock.location','rel_secondary_location', 'location', 'location_ids')
    sequence = fields.Integer()

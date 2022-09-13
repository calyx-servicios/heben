from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class StockWarehouse(models.Model):
    _inherit = 'stock.location'
    _order = 'sequence'

    name = fields.Char(required=False)
    contact = fields.Many2one('res.partner')
    zip_code_field = fields.Char("Postal Code")
    from_zip = fields.Char()
    to_zip = fields.Char()
    zip_code = fields.Char("Zip")
    wherehouse_id = fields.Many2one('stock.location')
    secondary_wherehouse_ids = fields.Many2many('stock.location','rel_secondary_wherehouse', 'wherehouse', 'wherehouse_ids')
    sequence = fields.Integer(default=10)

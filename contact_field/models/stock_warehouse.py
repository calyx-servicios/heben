from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    contact = fields.Many2one('res.partner')



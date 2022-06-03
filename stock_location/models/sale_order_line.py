from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    _order = "id desc"

    locations = fields.Many2one('stock.location')

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class StockBatchPicking(models.Model):
    """ This object allow to manage multiple stock.picking at the same time.
    """
    _inherit = ["stock.picking.batch"]
    _name = "stock.picking.batch"

    type_of_operation = fields.Selection([
        ('entry','Entry'),
        ('exit', 'Exit'),
        ],'Type of Operation', index=True, default='entry')

    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
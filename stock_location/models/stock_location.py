from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class StockWarehouse(models.Model):
    _inherit = 'stock.location'
    _order = 'sequence'

    name = fields.Char()
    contact = fields.Many2one('res.partner')
    zip_code_field = fields.Char(string=("Postal Code"))
    from_zip = fields.Char(string=("From Zip")
    to_zip = fields.Char(string=("To Zip")
    zip_code = fields.Char(string=("Zip")
    locations = fields.Many2one('stock.location')
    secondary_location = fields.One2many('stock.location', 'locations')
    sequence = fields.Integer(default=10)
    
    @api.constrains('secondary_location')
    def _secondary_location(self):
        if len(self.secondary_location) > 2:
            raise ValidationError(_('You can only add two locations'))

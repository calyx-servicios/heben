from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class StockWarehouse(models.Model):
    _inherit = 'stock.location'
    _order = 'sequence'

    contact = fields.Many2one('res.partner')
    zip_code_field = fields.Char(string=_("Postal Code"))
    from_zip = fields.Char(string=_("From Zip"))
    to_zip = fields.Char(string=_("To Zip"))
    zip_code = fields.Char(string=_("Zip"))
    warehouses = fields.Many2one('stock.location', string=_("Warehouses"))
    nearest_warehouse = fields.One2many('stock.location', 'warehouses', string=_("Nearest Warehouse"))
    sequence = fields.Integer(default=10)
    
    @api.constrains('nearest_warehouse')
    def _nearest_warehouse(self):
        if len(self.nearest_warehouse) > 2:
            raise ValidationError(_('You can only add two locations'))

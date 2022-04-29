from odoo import fields, models, _


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
    


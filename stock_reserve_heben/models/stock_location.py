from odoo import fields, models, _


class StockWarehouse(models.Model):
    _inherit = 'stock.location'
    _parent_name = "location_id"
    _order = 'sequence'

    name_location = fields.Char('Location Name', required=True)
    contact = fields.Many2one('res.partner')
    zip_code_field = fields.Char(string=_("Postal Code"))
    from_zip = fields.Char(string=_("From Zip"))
    to_zip = fields.Char(string=_("To Zip"))
    zip_code = fields.Char(string=_("Zip"))
    warehouses = fields.Many2one('stock.location', string=_("Warehouses"))
    nearest_warehouse = fields.One2many('stock.location', 'warehouses', string=_("Nearest Warehouse"))
    sequence = fields.Integer(required=True, default=2)
    location_id = fields.Many2one(
        'stock.location', 'Parent Location', index=True, ondelete='cascade',
        help="The parent location that includes this location. Example : The 'Dispatch Zone' is the 'Gate 1' parent location.")

    def name_get(self):
        ret_list = []
        for location in self:
            orig_location = location
            name = location.name
            while location.location_id and location.usage != 'view':
                location = location.location_id
                if not name:
                    raise UserError(_('You have to set a name for this location.'))
                name = location.name + "/" + name
            ret_list.append((orig_location.id, name))
        return ret_list

    @api.constrains('nearest_warehouse')
    def _nearest_warehouse(self):
        for record in self:
            if len(record.line_ids.ids) >= 2:
                raise ValidationError(_('you can only add two locations')))
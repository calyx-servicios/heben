from odoo import models,api,fields, _
from datetime import date
from odoo.exceptions import UserError

class StockPostBrach(models.Model):
    _name = 'stock.post.branch'

    code_nis = fields.Char('NIS')
    name  = fields.Char('Name')
    type_brach = fields.Char('Type')
    code_cpa = fields.Char('CPA')
    street = fields.Char('Street')
    street2 = fields.Char('Street2')
    zip = fields.Char('Zip', change_default=True)
    city = fields.Char('City')
    state_id = fields.Many2one("res.country.state", string='State')
    country_id = fields.Many2one('res.country', string='Country')
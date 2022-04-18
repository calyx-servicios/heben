from odoo import models, fields

class PartnerCode (models.Model):
    _inherit = 'res.partner'

    
    partner_code = fields.Char(string="Partner Code")



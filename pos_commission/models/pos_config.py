from odoo import fields, models

class PosConfig(models.Model):
    _inherit = 'pos.config'
    
    commission_type_rel = fields.Many2one('commission.type')


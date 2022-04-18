# -*- coding: utf-8 -*-
from odoo import models, fields, _


class PosConfig(models.Model):
    _inherit = 'pos.config'
    
    module_pos_seller = fields.Boolean(help=_("Show seller PoS session"))
    seller_ids = fields.Many2many(
        'hr.employee', 'hr_employee_seller_pos', 
        string=_("Seller with access"),
        help=_("If left empty, all sellers can be used in the POS session"))


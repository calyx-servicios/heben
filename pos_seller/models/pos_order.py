# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class PosOrder(models.Model):
    _inherit = "pos.order"

    seller_id = fields.Many2one('hr.employee', string=_('Seller'), 
        help="Person who makes the sale. It can be a reliever, a student or an interim employee.", states={'done': [('readonly', True)], 'invoiced': [('readonly', True)]})
    
    @api.model
    def _order_fields(self, ui_order):
        order_fields = super(PosOrder, self)._order_fields(ui_order)
        order_fields['seller_id'] = ui_order.get('seller_id')
        return order_fields


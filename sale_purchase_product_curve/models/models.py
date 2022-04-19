# -*- coding: utf-8 -*-

from odoo import models, fields, api


class sale_purchase_product_curve(models.Model):
    _name = 'sale.deyker'
    # _description = 'sale_purchase_product_curve.sale_purchase_product_curve'

#     name = fields.Char()
    value = fields.Char('VALUE ASD')
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

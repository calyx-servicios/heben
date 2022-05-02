# -*- coding: utf-8 -*-
from odoo import models, fields

class ProductCurve(models.Model):
    _inherit= 'sale.order'
      
    products_curve_ids = fields.Many2many(
        'product.template',
        'product_sale_order_curve_rel',
    )
        

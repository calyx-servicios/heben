# -*- coding: utf-8 -*-

from itertools import product
from odoo import models, fields, api

class AddProductCurve(models.Model):
    _inherit= 'sale.order'
    # _name = 'add.product.curve'
    
    button_save= fields.Boolean('Aplicar cambios')
    
    product_data_ids = fields.Many2many(
        'product.template',
        'product_sale_order_curve_rel',
    )
    
    product_save_data_ids = fields.Many2many(
        'product.template',
        # 'curve.product.template',
        'curve_product_template_rel'
    )
    
    product_template_att_data_ids = fields.Many2many(
        'product.template.attribute.line',
        # 'curve.product.template',
        'curve_product_template_attribute_line_rel'
    )
    
    
    #@api.onchange('product_data_ids')
    #def _onchange_button(self):
        #self.button = False
        #if self.product_data_ids:
            #print('*****+')
            #print('*****+')
            #print('*****+')
            #print('*****+')
            #print('*****+')
            
    #def _add_data_line(self):
        #pass
            
        

        

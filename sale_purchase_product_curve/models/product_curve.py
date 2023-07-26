# -*- coding: utf-8 -*-
from odoo import models, fields

class ProductCurveSale(models.Model):
    _inherit= 'sale.order'
      
    products_curve_ids = fields.Many2many(
        'product.template',
        'product_sale_order_curve_rel',
    )

class ProductCurveSaleTemplate(models.Model):
    _inherit= 'sale.order.template'
      
    products_curve_ids = fields.Many2many(
        'product.template',
        'product_sale_order_template_curve_rel',
    )

class ProductCurvePurchase(models.Model):
    _inherit= 'purchase.order'
      
    products_curve_ids = fields.Many2many(
        'product.template',
        'product_purchase_order_curve_rel',
    )

class ProductCurvePurchaseRequisition(models.Model):
    _inherit= 'purchase.requisition'
      
    products_curve_ids = fields.Many2many(
        'product.template',
        'product_purchase_requisition_curve_rel',
    )

class ProductCurveStockPicking(models.Model):
    _inherit= 'stock.picking'
      
    products_curve_ids = fields.Many2many(
        'product.template',
        'product_stock_picking_curve_rel',
    )

class ProductCurveStockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"
    
    products_curve_ids = fields.Many2many(
        'product.template',
        'product_stock_picking_batch_curve_rel',
    )


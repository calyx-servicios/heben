# -*- coding: utf-8 -*-
from odoo import fields, models, _
from datetime import datetime


class PosCommission(models.TransientModel):
    _name = "missing.picking.wizard"
    _description = "Missing Picking"
    

    product_imput_ids = fields.Many2many('stock.picking.batch.product')
    partner_id = fields.Many2one('res.partner')
    
    def creat_purchase_order(self):
        order = self.env['purchase.order'].create({'partner_id': self.partner_id.id,})
        order_lines = []
        for product in self.product_imput_ids:
            products = self.env['product.template'].sudo().search([('product_variant_ids', 'in', product.product_id.id)],limit=1)
            line = {
                'order_id': order.id,
                'product_id': product.product_id.id,
                'product_template_id': products.id,
                'name': product.product_id.display_name,
                'date_planned':datetime.now(),
                'product_qty': product.qty_left,
                'product_uom': product.product_id.uom_po_id.id,
                'price_unit': product.product_id.lst_price,
            }
            order_lines.append(line)
        order.order_line.create_multi(order_lines)
        return {
            'name': "Purchase order",
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'purchase.order',
            'target': 'new',
            'res_id': order.id,
        }
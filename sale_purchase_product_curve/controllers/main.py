# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request
from datetime import datetime

MODELS_STATUS = {
    'sale_order': ['draft','low'],
    'purchase_order': ['draft','low','in_out','liquidation'],
    'stock_move': ['draft','low'],
    'stock_picking_batch': ['draft','low'],
}

class AddProductCurve(http.Controller):
    @http.route(
        ['/get_data_product_curve'], 
        type="json", 
        auth="public",
    )
    def get_data_product_curve(self, **args):
        data = {'header':{},'rows':{}}
        product_id = args.get('id',  False)
        model = args.get('model', False)
        if product_id:
            product = request.env['product.template'].sudo().search([('id', '=', product_id)])
            if product.attribute_line_ids:
                matrix_template = product._get_template_matrix()
                products = request.env['product.product'].sudo().search([('product_tmpl_id', '=', product.id)])
                for values_prod in matrix_template.get('matrix'):
                    for val in values_prod:
                        ptav_ids = val.get('ptav_ids', False)
                        if ptav_ids != False and model != False:
                            status = MODELS_STATUS.get(model, 'sale_order')
                            for product in products:
                                product_attribute = product.product_template_attribute_value_ids.ids
                                product_attribute.sort() 
                                if (ptav_ids == product_attribute) and (product.state in status):
                                    val['is_possible_combination'] = False
                return matrix_template
            else:
                return False
        else:
            return False
        
    @http.route(
        ['/set_data_product_curve_sale'], 
        type="json", 
        auth="public",
    )
    def set_data_product_curve_sale(self, **args):
        data = args.get('data',  False)
        order_id = args.get('order_id',  False)
        if data and order_id:
            sl_obj = request.env['sale.order.line'].sudo()
            order_id = int(order_id)
            values = []
            for product in data:
                product_id = int(product['product_id'])
                product_tmpl = request.env['product.product'].search([('product_tmpl_id','=',product_id)])
                for line in product['lines']:
                    for variants in product_tmpl:
                        list_variant = line['variants'].split(',')
                        list_variant = list(map(int,list_variant))
                        variants_tmpl = variants.product_template_attribute_value_ids.ids
                        variants_tmpl.sort()
                        if list_variant == variants_tmpl:
                            line_exist = sl_obj.search([('order_id','=',order_id), ('product_id', '=', variants.id)])
                            if line_exist:
                                line_exist.product_uom_qty = line_exist.product_uom_qty + int(line['quantity'])
                            else:
                                dict_value = {
                                    'order_id': order_id,
                                    'product_id': variants.id, 
                                    'product_uom_qty': int(line['quantity'])
                                }
                                values.append(dict_value)
                        else:
                            continue   
                            
            if len(values) != 0:
                sl_obj.create_multi(values)
                return True
            else:
                return True
        else:
            return False
        
    @http.route(
        ['/set_data_product_curve_sale_template'], 
        type="json", 
        auth="public",
    )
    def set_data_product_curve_sale_template(self, **args):
        data = args.get('data',  False)
        order_id = args.get('order_id',  False)
        if data and order_id:
            stl_obj = request.env['sale.order.template.line'].sudo()
            order_id = int(order_id)
            values = []
            for product in data:
                product_id = int(product['product_id'])
                product_tmpl = request.env['product.product'].search([('product_tmpl_id','=',product_id)])
                for line in product['lines']:
                    for variants in product_tmpl:
                        list_variant = line['variants'].split(',')
                        list_variant = list(map(int,list_variant))
                        variants_tmpl = variants.product_template_attribute_value_ids.ids
                        variants_tmpl.sort()
                        if list_variant == variants_tmpl:
                            line_exist = stl_obj.search([('sale_order_template_id','=',order_id), ('product_id', '=', variants.id)])
                            if line_exist:
                                line_exist.product_uom_qty = line_exist.product_uom_qty + int(line['quantity'])
                            else:
                                dict_value = {
                                    'sale_order_template_id': order_id,
                                    'product_id': variants.id,
                                    'name': variants.display_name,
                                    'price_unit': variants.lst_price,
                                    'product_uom_id': variants.uom_po_id.id,
                                    'product_uom_qty': int(line['quantity'])
                                }
                                values.append(dict_value)
                        else:
                            continue   
                            
            if len(values) != 0:
                stl_obj.create_multi(values)
                return True
            else:
                return True
        else:
            return False

    @http.route(
        ['/set_data_product_curve_purchase'], 
        type="json", 
        auth="public",
    )
    def set_data_product_curve_purchase(self, **args):
        data = args.get('data',  False)
        order_id = args.get('order_id',  False)
        if data and order_id:
            pl_obj = request.env['purchase.order.line'].sudo()
            order_id = int(order_id)
            values = []
            for product in data:
                product_id = int(product['product_id'])
                product_tmpl = request.env['product.product'].search([('product_tmpl_id','=',product_id)])
                for line in product['lines']:
                    for variants in product_tmpl:
                        list_variant = line['variants'].split(',')
                        list_variant = list(map(int,list_variant))
                        variants_tmpl = variants.product_template_attribute_value_ids.ids
                        variants_tmpl.sort()
                        if list_variant == variants_tmpl:
                            line_exist = pl_obj.search([('order_id','=',order_id), ('product_id', '=', variants.id)])
                            if line_exist:
                                line_exist.product_uom_qty = line_exist.product_uom_qty + int(line['quantity'])
                            else:
                                dict_value = {
                                    'order_id': order_id,
                                    'product_id': variants.id,
                                    'product_template_id': product_id,
                                    'name': variants.display_name,
                                    'date_planned':datetime.now(),
                                    'product_qty': int(line['quantity']),
                                    'product_uom': variants.uom_po_id.id,
                                    'price_unit': variants.lst_price,
                                    'taxes_id': [(6, 0, variants.supplier_taxes_id.ids)],
                                }
                                values.append(dict_value)
                        else:
                            continue   
                            
            if len(values) != 0:
                pl_obj.create_multi(values)
                return True
            else:
                return True
        else:
            return False

    @http.route(
        ['/set_data_product_curve_prequisition'], 
        type="json", 
        auth="public",
    )
    def set_data_product_curve_prequisition(self, **args):
        data = args.get('data',  False)
        order_id = args.get('order_id',  False)
        if data and order_id:
            prl_obj = request.env['purchase.requisition.line'].sudo()
            order_id = int(order_id)
            values = []
            for product in data:
                product_id = int(product['product_id'])
                product_tmpl = request.env['product.product'].search([('product_tmpl_id','=',product_id)])
                for line in product['lines']:
                    for variants in product_tmpl:
                        list_variant = line['variants'].split(',')
                        list_variant = list(map(int,list_variant))
                        variants_tmpl = variants.product_template_attribute_value_ids.ids
                        variants_tmpl.sort()
                        if list_variant == variants_tmpl:
                            line_exist = prl_obj.search([('requisition_id','=',order_id), ('product_id', '=', variants.id)])
                            if line_exist:
                                line_exist.product_uom_qty = line_exist.product_uom_qty + int(line['quantity'])
                            else:
                                dict_value = {
                                    'requisition_id': order_id,
                                    'product_id': variants.id,
                                    'price_unit': variants.lst_price,
                                    'product_uom_id': variants.uom_po_id.id,
                                    'product_qty': int(line['quantity'])
                                }
                                values.append(dict_value)
                        else:
                            continue   
                            
            if len(values) != 0:
                prl_obj.create_multi(values)
                return True
            else:
                return True
        else:
            return False

    @http.route(
        ['/set_data_product_curve_stock_move'], 
        type="json", 
        auth="public",
    )
    def set_data_product_curve_stock_move(self, **args):
        data = args.get('data',  False)
        picking_id = args.get('order_id',  False)
        if data and picking_id:
            sm_obj = request.env['stock.move'].sudo()
            picking_id = int(picking_id)
            picking = request.env['stock.picking'].sudo().search([('id', '=',picking_id)])
            values = []
            for product in data:
                product_id = int(product['product_id'])
                product_tmpl = request.env['product.product'].search([('product_tmpl_id','=',product_id)])
                for line in product['lines']:
                    for variants in product_tmpl:
                        list_variant = line['variants'].split(',')
                        list_variant = list(map(int,list_variant))
                        variants_tmpl = variants.product_template_attribute_value_ids.ids
                        variants_tmpl.sort()
                        if list_variant == variants_tmpl:
                            line_exist = sm_obj.search([('picking_id','=',picking_id), ('product_id', '=', variants.id)])
                            if line_exist:
                                line_exist.product_uom_qty = line_exist.product_uom_qty + int(line['quantity'])
                            else:
                                dict_value = {
                                    'name': _('New Move:') + variants.display_name,
                                    'product_id': variants.id,
                                    'product_uom_qty': int(line['quantity']),
                                    'product_uom': variants.uom_po_id.id,
                                    'location_id': picking.location_id.id,
                                    'location_dest_id': picking.location_dest_id.id,
                                    'state': 'draft',
                                    'additional': True,
                                    'picking_id': picking_id
                                }
                                values.append(dict_value)
                        else:
                            continue   
                            
            if len(values) != 0:
                sm_obj.create_multi(values)
                return True
            else:
                return True
        else:
            return False

    @http.route(
        ['/set_data_product_curve_stock_picking_batch'], 
        type="json", 
        auth="public",
    )
    def set_data_product_curve_stock_picking_batch(self, **args):
        data = args.get('data',  False)
        batch_id = args.get('batch_id',  False)
        if data and batch_id:
            spbp_obj = request.env['stock.picking.batch.product'].sudo()
            batch_id = int(batch_id)
            values = []
            for product in data:
                product_id = int(product['product_id'])
                product_tmpl = request.env['product.product'].search([('product_tmpl_id','=',product_id)])
                for line in product['lines']:
                    for variants in product_tmpl:
                        list_variant = line['variants'].split(',')
                        list_variant = list(map(int,list_variant))
                        variants_tmpl = variants.product_template_attribute_value_ids.ids
                        variants_tmpl.sort()
                        if list_variant == variants_tmpl:
                            line_exist = spbp_obj.search([('batch_id','=',batch_id), ('product_id', '=', variants.id)])
                            if line_exist:
                                line_exist.qty = line_exist.qty + int(line['quantity'])
                            else:
                                dict_value = {
                                    'batch_id': batch_id,
                                    'product_id': variants.id,
                                    'qty': int(line['quantity'])
                                }
                                values.append(dict_value)
                        else:
                            continue   
                            
            if len(values) != 0:
                spbp_obj.create_multi(values)
                return True
            else:
                return True
        else:
            return False


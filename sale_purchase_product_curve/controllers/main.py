# -*- coding: utf-8 -*-
from odoo.http import request
from odoo import http
from datetime import datetime


class AddProductCurve(http.Controller):
    @http.route(
        ['/get_data_product_curve'], 
        type="json", 
        auth="public",
    )
    def get_data_product_curve(self, **args):
        data = {'header':{},'rows':{}}
        product_id = args.get('id',  False)
        if product_id:
            product = request.env['product.template'].sudo().search([('id', '=', product_id)])
            if product.attribute_line_ids:
                return product._get_template_matrix()
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
                                    'price_unit': variants.lst_price
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


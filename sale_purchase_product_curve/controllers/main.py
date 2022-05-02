# -*- coding: utf-8 -*-
from odoo.http import request
from odoo import http


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
        ['/set_data_product_curve'], 
        type="json", 
        auth="public",
    )
    def set_data_product_curve(self, **args):
        data = args.get('data',  False)
        order_id = args.get('order_id',  False)
        if data and order_id:
            sl_obj = request.env['sale.order.line'].sudo()
            so_obj = request.env['sale.order'].sudo()
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


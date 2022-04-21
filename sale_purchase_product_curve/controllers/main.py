# -*- coding: utf-8 -*-

from odoo.http import request
from odoo import http
import json


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


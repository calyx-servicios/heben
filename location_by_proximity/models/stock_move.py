from odoo import models

class StockMove(models.Model):
    _inherit = "stock.move"

    def create(self, vals_list):
        so = False
        if type(vals_list) != type({}):
            if vals_list[0].get('origin',False):
                so = self.env['sale.order'].search([('name','=',vals_list[0]['origin'])])
                if so:
                    so_lines = so.order_line
                    for order_line in so.order_line:
                        if order_line.product_id.type == 'service':
                            so_lines -= order_line
                    if so_lines:
                        for vals_line,so_line in zip(vals_list,so_lines):
                            vals_line['location_id'] = so_line.location_id.id    
        else:
            if vals_list.get('origin',False):
                so = self.env['sale.order'].search([('name','=',vals_list['origin'])])
                if so:
                    so_lines = so.order_line
                    for order_line in so.order_line:
                        if order_line.product_id.type == 'service':
                            so_lines -= order_line
                    if so_lines:
                        vals_list['location_id'] = so_line.location_id.id    
    
        return super().create(vals_list)
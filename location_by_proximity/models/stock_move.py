from odoo import models

class StockMove(models.Model):
    _inherit = "stock.move"

    def create(self, vals_list):
        so = self.env['sale.order'].search([('name','=',vals_list[0]['origin'])])
        if so:
            so_lines = so.order_line
            if so_lines:
                for vals_line,so_line in zip(vals_list,so_lines):
                    vals_line['location_id'] = so_line.location_id.id
        res = super().create(vals_list)
        return res
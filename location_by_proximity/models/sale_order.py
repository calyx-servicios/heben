from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def check_location(self):
        client_zip = int(self.partner_id.zip)
        master_location = self.env['stock.location'].search([('from_zip','<=',client_zip),('to_zip','>=',client_zip)])
        locations = master_location + master_location.secondary_location_ids
        order_lines = self.order_line
        order_lines.write({
                'location_id':False
            })
        for order_line in order_lines:
            house_empty = False
            for location in locations:
                if order_line.product_uom_qty <= self.env['stock.quant'].search([('product_id','=',order_line.product_id.id),('location_id','=',location.id)]).quantity:
                    order_line.location_id = location.id
                    house_empty = True
                    break
            if not house_empty:
                msg='For the product ' + order_line.name  + ' there is no stock in the selected locations'
                self.message_post(body=msg)

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    _order = "id desc"

    location_id = fields.Many2one('stock.location')



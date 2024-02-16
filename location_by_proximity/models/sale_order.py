from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def check_location(self):
        client_zip = int(self.partner_id.zip)
        master_location = self.env['stock.location'].search([('from_zip','<=',client_zip),('to_zip','>=',client_zip)])
        locations = master_location + master_location.secondary_location_ids
        order_lines = self.order_line
        for order_line in self.order_line:
            if order_line.product_id.type == 'service':
                order_lines -= order_line
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
                self.send_chat(order_line.order_id.user_id, order_line.order_id.partner_id, msg, order_line.product_id.name)
                return False
        return True
    
    def action_confirm(self):
        lines_product = self.order_line.filtered(lambda x: x.product_id.type != 'service')
        if lines_product:
            lines_unlocated = lines_product.filtered(lambda l: not l.location_id)
            if lines_unlocated:
                order_id = lines_unlocated.mapped("order_id")
                if not order_id.partner_id.zip:
                    for line in lines_unlocated:
                        line.location_id = order_id.warehouse_id.lot_stock_id.id
                else:
                    if not order_id.check_location():
                        return
        if not self.user_id:
            self.user_id = self.env.user.id
        return super(SaleOrder, self).action_confirm()


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    _order = "id desc"

    location_id = fields.Many2one('stock.location')


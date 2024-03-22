from odoo import models

class GtMagentoStore(models.Model):
    _inherit = "gt.magento.store"

    def update_orders_status(self):
        order_ids = self.env['sale.order'].search([
            ('order_status','!=', 'completed'),
            ('order_status','!=', 'canceled'),
            ('ma_order_id','!=', False)
        ])
        
        self.GtUpdateMagentoOrders(order_ids)
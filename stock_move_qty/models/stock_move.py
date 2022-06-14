from odoo import models, api

class StockMove(models.Model):
    _inherit = "stock.move"

    def _set_product_uom_qty(self):
        if self.product_id:
            self.product_uom_qty = 1
        else:
            self.product_uom_qty = 0.0
    
    @api.onchange('product_id', 'picking_type_id')
    def onchange_product(self):
        if self.product_id:
            product = self.product_id.with_context(lang=self.picking_id.partner_id.lang or self.env.user.lang)
            self.description_picking = product._get_description(self.picking_type_id)
            self._set_product_uom_qty()


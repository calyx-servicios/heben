from odoo import fields, models, api


class StockPickingBatchProduct(models.Model):
    _inherit = "stock.picking.batch.product"

    @api.model
    def create_multi(self, list_vals):
        # list_vals: list of dictionary [{}, {}, {}.....]
        rec_ids = []
        for val in list_vals:
            # Call create method of current object (stock.picking.batch)
            rec_ids.append(self.create(val).id)
        # Return list of IDs
        return rec_ids


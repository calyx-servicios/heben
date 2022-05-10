from odoo import models, api

class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    @api.model
    def create_multi(self, list_vals):
        # list_vals: list of dictionary [{}, {}, {}.....]
        rec_ids = []
        for val in list_vals:
            # Call create method of current object (purchase.order.line)
            rec_ids.append(self.create(val).id)
        # Return list of IDs
        return rec_ids


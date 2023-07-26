from odoo import models


class PickingInvoiceWizard(models.TransientModel):
    _inherit = 'picking.invoice.wizard'

    def picking_multi_invoice(self):
        pick_obj = self.env['stock.picking']
        active_ids = self.env.context.get('active_ids')
        if len(active_ids) != 0:
            picking_ids = pick_obj.browse(active_ids)
            pickings = picking_ids.filtered(lambda x: x.state == 'done' and x.invoice_count == 0)
            if len(pickings) != 0:
                pick_in = pickings.filtered(lambda p: p.picking_type_id.code == 'incoming' and not p.is_return)
                if len(pick_in) != 0:
                    pick_in.create_bill()
                pick_out = pickings.filtered(lambda p: p.picking_type_id.code == 'outgoing' and not p.is_return)
                if len(pick_out) != 0:
                    pick_out.create_invoice()
                pick_in_return = pickings.filtered(lambda p: p.picking_type_id.code == 'incoming' and p.is_return)
                if len(pick_in_return) != 0:
                    pick_in_return.create_bill('in_refund')
                pick_out_return = pickings.filtered(lambda p: p.picking_type_id.code == 'outgoing' and p.is_return)
                if len(pick_out_return) != 0:
                    pick_out_return.create_invoice('out_refund')


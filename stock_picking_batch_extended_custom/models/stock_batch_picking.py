from odoo import fields, models


class StockBatchPicking(models.Model):
    _inherit = "stock.picking.batch"

    type_of_operation = fields.Selection([
        ('entry','Entry'),
        ('exit', 'Exit'),
        ],'Type of Operation', index=True, default='entry')

    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    product_imput_ids = fields.One2many('stock.picking.batch.product',inverse_name="batch_id")
    import_completed = fields.Boolean()

    def compute_import(self):
        move_lines = []
        reserved_availability = []
        pickings_to_process = []
        for line in self.product_imput_ids:
            qty_to_do = line.qty
            line.qty_left = line.qty
            pickings = self.env['stock.picking'].search([('state','=',"assigned"),('partner_id','=',self.partner_id.id)], order='date')
            for picking in pickings:
                move_line = picking.move_ids_without_package.filtered(lambda picking_line: picking_line.product_id.id == line.product_id.id)
                if len(move_line) != 0 and qty_to_do != 0:
                    if move_line.product_uom_qty >= qty_to_do:
                        move_lines.append(move_line)
                        reserved_availability.append(qty_to_do)
                        qty_to_do = 0
                        line.qty_left = 0
                        pickings_to_process.append(picking)
                    else:
                        move_lines.append(move_line)
                        reserved_availability.append(move_line.product_uom_qty)
                        qty_to_do = qty_to_do - move_line.product_uom_qty
                        line.qty_left = qty_to_do
                        pickings_to_process.append(picking)
        incomplete_poducts = self.product_imput_ids.filtered(lambda product_name: product_name.qty_left != 0)
        if len(incomplete_poducts.ids) != 0:
            return {
                    'name': "Something went wrong!",
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_model': 'missing.picking.wizard',
                    'view_id': self.env.ref('stock_picking_batch_extended_custom.missing_picking_wizard_view_form').id,
                    'target': 'new',
                    'context': {
                        'default_product_imput_ids': incomplete_poducts.ids,
                        'default_partner_id': self.partner_id.id,
                    }}
        else:
            for picking_line, qty_done in zip(move_lines,reserved_availability):
                picking_line.reserved_availability = qty_done
        pickings_to_process = list(dict.fromkeys(pickings_to_process))
        for picking_to_process in pickings_to_process:
            self.picking_ids += picking_to_process
            values = {'pick_ids': picking_to_process}
            sit = self.env['stock.backorder.confirmation'].create(values)
            sit.process()

class StockBatchPickingProduct(models.Model):
    _name = "stock.picking.batch.product"
    _description = "Stock Picking batch product"

    batch_id = fields.Many2one('stock.picking.batch')
    product_id = fields.Many2one('product.product')
    qty = fields.Integer()
    qty_left = fields.Integer()

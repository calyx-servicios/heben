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
        for line in self.product_imput_ids:
            qty_to_do = line.qty
            pickings = self.env['stock.picking'].search([('state','=',"assigned"),('partner_id','=',self.partner_id.id)], order='date')
            for picking in pickings:
                move_line = picking.move_ids_without_package.filtered(lambda picking_line: picking_line.product_id.id == line.product_id.id)
                if len(move_line) != 0 and qty_to_do != 0:
                    if move_line.product_uom_qty >= qty_to_do:
                        move_line.quantity_done = qty_to_do
                        qty_to_do = 0
                        values = {'pick_ids': picking}
                        sit = self.env['stock.backorder.confirmation'].create(values)
                        sit.process()
                        self.picking_ids += picking
                    else:
                        move_line.quantity_done = move_line.product_uom_qty
                        qty_to_do = qty_to_do - move_line.product_uom_qty
                        values = {'pick_ids': picking}
                        sit = self.env['stock.backorder.confirmation'].create(values)
                        sit.process()
                        self.picking_ids += picking

class StockBatchPickingProduct(models.Model):
    _name = "stock.picking.batch.product"
    _description = "Stock Picking batch product"

    batch_id = fields.Many2one('stock.picking.batch')
    product_id = fields.Many2one('product.product')
    qty = fields.Integer()


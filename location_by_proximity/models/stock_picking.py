from odoo import models, fields, api

class CustomStockPicking(models.Model):
    _inherit = 'stock.picking'

    # Campo para marcar si el action_assign debe ser ignorado
    ma_action_assign_ignored = fields.Boolean(default=False)

    @api.model
    def create(self, vals):
        sale_order = self.env['sale.order'].search([('name', '=', vals.get('origin', False))], limit=1)
        if sale_order and sale_order.ma_order_id:
            vals['state'] = 'confirmed'
            vals['ma_action_assign_ignored'] = True  # Marcar para ignorar el primer action_assign
        return super(CustomStockPicking, self).create(vals)

    def action_assign(self):
        if self.ma_action_assign_ignored:
            # Si ya se marcó para ignorar, permitir el funcionamiento normal de action_assign
            self.ma_action_assign_ignored = False  # Resetear la bandera para permitir futuras llamadas normales
            return True
        else:
            return super(CustomStockPicking, self).action_assign()

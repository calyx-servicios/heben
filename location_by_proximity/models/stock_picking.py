from odoo import models, fields, api

class CustomStockPicking(models.Model):
    _inherit = 'stock.picking'

    # Campo para marcar si el action_assign debe ser ignorado
    ma_action_assign_ignored = fields.Boolean(default=False)

    @api.model
    def action_assign(self):
        if self.ma_action_assign_ignored:
            self.ma_action_assign_ignored = False  # Resetear la bandera para permitir futuras llamadas normales
            return True
        else:
            return super(CustomStockPicking, self).action_assign()

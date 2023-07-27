from odoo import models, api, fields

class AccountPaymentGroup(models.Model):
    _inherit = "account.payment.group"

    retencion_ganancias = fields.Selection([
        ('imposibilidad_retencion', 'Imposibilidad de Retención'),
        ('no_aplica', 'No Aplica'),
        ('nro_regimen', 'Nro Regimen'),
    ],
        'Retención Ganancias',
        default='no_aplica',
        readonly=True,
        states={'draft': [('readonly', False)],
                'confirmed': [('readonly', False)]}
    )

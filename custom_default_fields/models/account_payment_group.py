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

    @api.onchange('retencion_ganancias')
    def on_change_retencion_ganancias(self):
        if self.retencion_ganancias == 'no_aplica':
            self.regimen_ganancias_id = False
        elif self.retencion_ganancias == 'nro_regimen':
            cia_regs = self.company_regimenes_ganancias_ids
            partner_regimen = (
                self.commercial_partner_id.default_regimen_ganancias_id)
            if partner_regimen:
                def_regimen = partner_regimen
            elif cia_regs:
                def_regimen = cia_regs[0]
            else:
                def_regimen = False
            self.regimen_ganancias_id = def_regimen

    @api.onchange('commercial_partner_id')
    def change_retencion_ganancias(self):
        pass

    @api.onchange('company_regimenes_ganancias_ids')
    def change_company_regimenes_ganancias(self):
        pass

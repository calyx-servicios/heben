from odoo import models, fields, _


class AccountJournal(models.Model):
    _inherit = 'account.journal'
    
    is_commission = fields.Boolean(default=False)


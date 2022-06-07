from odoo import models, fields


class AccountJournal(models.Model):
    _inherit = 'account.journal'
    
    is_commission = fields.Boolean(default=False)


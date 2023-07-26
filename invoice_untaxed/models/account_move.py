from odoo import models, api


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.onchange('journal_id')
    def _onchange_journal(self):
        super(AccountMove, self)._onchange_journal()
        line = self.invoice_line_ids.filtered(lambda l: l.tax_ids)
        line._onchange_product_id()
        line.recompute_tax_line = True
        self._recompute_dynamic_lines(recompute_tax_base_amount=True)
    

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"
    
    def _get_computed_taxes(self):
        tax_ids = super(AccountMoveLine, self)._get_computed_taxes()
        if self.move_id.journal_id and not self.move_id.journal_id.l10n_latam_use_documents:
            tax_ids = [(5,0,0)]
        return tax_ids


from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    def _create_invoices(self, grouped=False, final=False):
        moves = super(SaleOrder, self)._create_invoices(grouped, final)
        for invoice in moves:
            if invoice.journal_id and not invoice.journal_id.l10n_latam_use_documents:
                for line in invoice.invoice_line_ids:
                    line.tax_ids = [(5,0,0)]
        return moves


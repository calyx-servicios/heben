# -*- coding: utf-8 -*-
from odoo import fields, models, _

class PosCommission(models.TransientModel):
    _name = "pos.commission.wizard"
    _description = _("Create invoices from commissions")
    
    def _prepare_invoice_values(self, commission):
        invoice_vals = {
            'type': 'in_invoice',
            'invoice_origin': commission['order'],
            'partner_id': commission['partner_id'],
            'invoice_line_ids': commission['invoice_lines'],
        }
        if commission.get('journal_id', False):
            invoice_vals['journal_id'] = commission['journal_id']

        return invoice_vals
    
    def _prepare_invoice_line_values(self, invoice_line_vals):
        invoice_lines_values = []
        for line in invoice_line_vals:
            invoice_lines_values.append(
                (0, 0, {
                    'name': line['description'],
                    'price_unit': line['amount'],
                    'quantity': 1.0,
                })
            )
        return invoice_lines_values
    
    
    def create_invoices(self):
        commission_line_obj = self.env['commission.line'].sudo() 
        commission_lines = commission_line_obj.browse(self._context.get('active_ids', []))
        values = {}
        
        for commission in commission_lines:
            if commission.sellers:
                seller_id = commission.sellers.user_partner_id.id
                description = commission.commission.name + ' - ' + dict(commission_line_obj._fields['commission_type'].selection).get(commission.commission_type)
                amount = commission.amount
                company = commission.sellers.company_id.id
                journal = self.env['account.journal'].search([
                    ('type', '=', 'purchase'),
                    ('is_commission','=',True),
                    ('company_id','=',company)
                ],limit=1)
                if values.get(seller_id, False):
                    values[seller_id]['invoice_lines'].append({
                        'amount': amount, 'description': description
                    })
                    values[seller_id]['commission_lines'].append(commission)
                else:
                    values[seller_id] = {
                        'order': commission.order.name, 'partner_id': seller_id, 
                        'commission_lines': [commission],
                        'invoice_lines': [{'amount': amount, 'description': description}]
                    }
                    if journal:
                        values[seller_id]['journal_id'] = journal.id
            else:
                boss_id = commission.bosses.user_partner_id.id
                description = commission.commission.name + ' - ' + dict(commission_line_obj._fields['commission_type'].selection).get(commission.commission_type)
                amount = commission.amount
                company = commission.bosses.company_id.id
                journal = self.env['account.journal'].search([
                    ('type', '=', 'purchase'),
                    ('is_commission','=',True),
                    ('company_id','=',company)
                ],limit=1)
                if values.get(boss_id, False):
                    values[boss_id]['invoice_lines'].append({
                        'amount': amount, 'description': description
                    })
                    values[boss_id]['commission_lines'].append(commission)
                else:
                    values[boss_id] = {
                        'order': commission.order.name, 'partner_id': boss_id, 
                        'commission_lines': [commission],
                        'invoice_lines': [{'amount': amount, 'description': description}]
                    }
                    if journal:
                        values[boss_id]['journal_id'] = journal.id
            
        for partner in values:
            commision_lines = values[partner].pop('commission_lines')
            invoice_lines_vals = values[partner].pop('invoice_lines')
            invoice_lines = self._prepare_invoice_line_values(invoice_lines_vals)
            values[partner]['invoice_lines'] = invoice_lines
            invoice_vals = self._prepare_invoice_values(values[partner])
            invoice = self.env['account.move'].sudo().create(invoice_vals).with_user(self.env.uid)
            for line in commision_lines:
                line.invoice_ids = [(4, invoice.id)]
                line.active = False

        if self._context.get('open_invoices', False):
            return commission_lines.action_view_invoice()
        return {'type': 'ir.actions.act_window_close'}


from odoo import models, _
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'


    def create_invoice(self, type='out_invoice'):
        """This is the function for creating customer invoice from the picking"""
        customer_journal_id = self.env['ir.config_parameter'].sudo().get_param('stock_move_invoice.customer_journal_id') or False
        if not customer_journal_id:
            raise UserError(_("Please configure the journal from settings"))
        current_user = self.env.uid
        invoice_line_list = []
        invoice_origin_names = ""
        for picking_id in self:
            if len(invoice_origin_names) == 0:
                invoice_origin_names += picking_id.name
            else:
               invoice_origin_names += ", " + picking_id.name
            if picking_id.sale_id:
                origin_doc = picking_id.sale_id
            elif picking_id.purchase_id:
                origin_doc = picking_id.purchase_id
            else:
                origin_doc = False
            
            if origin_doc:
                for line_id in picking_id.move_ids_without_package.filtered(lambda m: m.state == 'done'):
                    product = origin_doc.order_line.filtered(lambda l: l.product_id.id == line_id.product_id.id)
                    if product:
                        vals = (0, 0, {
                            'name': line_id.description_picking,
                            'product_id': line_id.product_id.id,
                            'price_unit': product.price_unit if len(product) != 0 else line_id.product_id.lst_price ,
                            'account_id': line_id.product_id.property_account_income_id.id if line_id.product_id.property_account_income_id
                                else line_id.product_id.categ_id.property_account_income_categ_id.id,
                            'tax_ids': [(6, 0, [picking_id.company_id.account_sale_tax_id.id])],
                            'quantity': line_id.quantity_done,
                        })
                        invoice_line_list.append(vals)

        invoice = self.env['account.move'].create({
            'type': type,
            'invoice_origin': invoice_origin_names,
            'invoice_user_id': current_user,
            'narration': invoice_origin_names,
            'partner_id': picking_id.partner_id.id,
            'currency_id': self.env.user.company_id.currency_id.id,
            'journal_id': int(customer_journal_id),
            'invoice_payment_ref': invoice_origin_names,
            'invoice_line_ids': invoice_line_list,
            'picking_ids': [(6, 0, self.ids)]
        })
        return invoice

    def create_bill(self, type='in_invoice'):
        """This is the function for creating vendor bill from the picking"""
        vendor_journal_id = self.env['ir.config_parameter'].sudo().get_param('stock_move_invoice.vendor_journal_id') or False
        if not vendor_journal_id:
            raise UserError(_("Please configure the journal from settings"))
        current_user = self.env.uid
        invoice_line_list = []
        invoice_origin_names = ""
        for picking_id in self:
            if len(invoice_origin_names) == 0:
                invoice_origin_names += picking_id.name
            else:
               invoice_origin_names += ", " + picking_id.name
               
            if picking_id.sale_id:
                origin_doc = picking_id.sale_id
            elif picking_id.purchase_id:
                origin_doc = picking_id.purchase_id
            else:
                origin_doc = False
            
            if origin_doc:
                for line_id in picking_id.move_ids_without_package.filtered(lambda m: m.state == 'done'):
                    product = origin_doc.order_line.filtered(lambda l: l.product_id.id == line_id.product_id.id)
                    if product:
                        vals = (0, 0, {
                            'name': line_id.description_picking,
                            'product_id': line_id.product_id.id,
                            'price_unit': product.price_unit if len(product) != 0 else line_id.product_id.lst_price ,
                            'account_id': line_id.product_id.property_account_income_id.id if line_id.product_id.property_account_income_id
                                else line_id.product_id.categ_id.property_account_income_categ_id.id,
                            'tax_ids': [(6, 0, [picking_id.company_id.account_sale_tax_id.id])],
                            'quantity': line_id.quantity_done,
                        })
                        invoice_line_list.append(vals)
 
        invoice = self.env['account.move'].create({
            'type': type,
            'invoice_origin': invoice_origin_names,
            'invoice_user_id': current_user,
            'narration': invoice_origin_names,
            'partner_id': picking_id.partner_id.id,
            'currency_id': self.env.user.company_id.currency_id.id,
            'journal_id': int(vendor_journal_id),
            'invoice_payment_ref': invoice_origin_names,
            'invoice_line_ids': invoice_line_list,
            'picking_ids': [(6, 0, self.ids)]
        })
        return invoice


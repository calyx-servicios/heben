from odoo import fields, models, _


class CommissionLine(models.Model):
    _name = 'commission.line'
    _description = "Commission line"

    order = fields.Many2one('pos.order')
    sellers = fields.Many2one('hr.employee', string=_("Seller"))
    commission = fields.Many2one('commission.type')
    commission_type = fields.Selection([
        ('standard', 'Standard'),
        ('product_categ', 'Product or Category'),
        ], string=_('Commission Type'), default='standard',
        help=_("Standard - Commission will be provided as percentage or fixed amount.\n") +
            _("Product or Category - Commission will be provided as percentage or fixed amount.\n"))
    product_id = fields.Many2many(
        'product.product', string=_('Product Variant'),
        help=_("Specify a product if this rule only applies to one product. Keep empty otherwise."))
    categ_id = fields.Many2many(
        'product.category', string=_('Product Category'),
        help=_("Specify a product category if this rule only applies to products belonging to this category or its children categories. Keep empty otherwise."))
    product_tmpl_id = fields.Many2many(
        'product.template', string=_('Product'),
        help=_("Specify a template if this rule only applies to one product template. Keep empty otherwise."))
    amount = fields.Float()
    tree_product_tmpl = fields.Char(string=_("Product Variant"))
    tree_category = fields.Char(string=_("Product Category"))
    tree_product = fields.Char(string=_("Product"))
    active = fields.Boolean(default=True)
    invoice_ids = fields.Many2many("account.move", string='Invoices', readonly=True, copy=False)
    company = fields.Char(string=_('Company'))
    store = fields.Char(string=_('Store'))
    point_of_sale = fields.Char(string=_('Point of sale'))
    
    def action_view_invoice(self):
        invoices = self.mapped('invoice_ids')
        action = self.env.ref('account.action_move_in_invoice_type').read()[0]
        if len(invoices) > 1:
            action['domain'] = [('id', 'in', invoices.ids)]
        elif len(invoices) == 1:
            form_view = [(self.env.ref('account.view_move_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = invoices.id
        else:
            action = {'type': 'ir.actions.act_window_close'}

        context = {
            'default_type': 'in_invoice',
        }

        if len(self) == 1:
            context.update({
                'default_partner_id': self.sellers.user_partner_id.id,
                'default_partner_shipping_id': self.sellers.id,
                'default_invoice_payment_term_id': self.env['account.move'].default_get(['invoice_payment_term_id']).get('invoice_payment_term_id'),
                'default_invoice_origin': self.order.name,
                'default_user_id': self.sellers.user_id.id,
            })
        action['context'] = context
        return action

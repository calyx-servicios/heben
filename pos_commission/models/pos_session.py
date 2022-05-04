from odoo import models


class PosSession(models.Model):
    _inherit = 'pos.session'

    def action_pos_session_closing_control(self):
        pos_orders = self.env['pos.order'].search([('session_id','=', self.id), ('state','=','paid')])
        for pos_order in pos_orders:
            if pos_order.seller_id:
                active_commissions = self.env['commission.type'].search([('active','=',True),('sellers_ids','in',pos_order.seller_id.id)])
                if active_commissions:
                    for active_commission in active_commissions:
                        commission_line = {
                                            'sellers':pos_order.seller_id.id,
                                            'commission':active_commission.id,
                                            'order':pos_order.id,
                                            'company': ','.join([c.name for c in active_commission.company_id]),
                                            'store': ','.join([s.name for s in active_commission.store_id]),
                                            'point_of_sale': ','.join([pos.name for pos in active_commission.point_of_sale_id]),
                                            }
                        if active_commission.commission_type == 'standard':
                            commission_line['commission_type'] = 'standard'
                            commission_line['tree_product'] = 'All Products'
                            if active_commission.standard_commission_type == 'percentage':
                                commission_line['amount'] = pos_order.amount_paid * active_commission.percentage_commission / 100
                                self.env['commission.line'].create(commission_line)
                            else:
                                commission_line['amount'] = active_commission.fixed_commission
                                self.env['commission.line'].create(commission_line)
                        else:
                            commission_line['commission_type'] = 'product_categ'
                            for commission_lines in active_commission.commission_line_ids:
                                if commission_lines.applied_on == '3_global':
                                    if commission_lines.compute_price == 'percentage':
                                        commission_line['amount'] = pos_order.amount_paid * commission_lines.percent_price / 100
                                        self.env['commission.line'].create(commission_line)
                                    else:
                                        commission_line['amount'] = commission_lines.fixed_price * len(pos_order.lines.ids)
                                        self.env['commission.line'].create(commission_line)
                                if commission_lines.applied_on == '2_product_category':
                                    if len(commission_lines.categ_id) == 1:
                                        commission_line['tree_category'] = commission_lines.categ_id[0].name
                                    elif len(commission_lines.categ_id) == 0:
                                        commission_line['tree_category'] = ""
                                    else:
                                        commission_line['tree_category'] = "Multiple"
                                    amount = 0
                                    for line in pos_order.lines:
                                        if line.product_id.categ_id in commission_lines.categ_id:
                                            if commission_lines.compute_price == 'percentage':
                                                amount += (line.price_subtotal_incl * commission_lines.percent_price / 100)
                                            else:
                                                amount += commission_lines.fixed_price
                                    if amount != 0:
                                        commission_line['amount'] = amount
                                        self.env['commission.line'].create(commission_line)
                                if commission_lines.applied_on == '1_product':
                                    amount = 0
                                    if len(commission_lines.product_tmpl_id.ids) == 1:
                                        commission_line['tree_category'] = commission_lines.product_tmpl_id[0].name
                                    elif len(commission_lines.product_tmpl_id.ids) == 0:
                                        commission_line['tree_category'] = ""
                                    else:
                                        commission_line['tree_category'] = "Multiple"
                                    for line in pos_order.lines:
                                        if line.product_id.product_tmpl_id in commission_lines.product_tmpl_id:
                                            if commission_lines.compute_price == 'percentage':
                                                amount += (line.price_subtotal_incl * commission_lines.percent_price / 100)
                                            else:
                                                amount += commission_lines.fixed_price
                                    if amount != 0:
                                        commission_line['amount'] = amount
                                        self.env['commission.line'].create(commission_line)
                                if commission_lines.applied_on == '0_product_variant':
                                    amount = 0
                                    if len(commission_lines.product_id.ids) == 1:
                                        commission_line['tree_category'] = commission_lines.product_id[0].name
                                    elif len(commission_lines.product_id.ids) == 0:
                                        commission_line['tree_category'] = ""
                                    else:
                                        commission_line['tree_category'] = "Multiple"
                                    for line in pos_order.lines:
                                        if line.product_id in commission_lines.product_id:
                                            if commission_lines.compute_price == 'percentage':
                                                amount += (line.price_subtotal_incl * commission_lines.percent_price / 100)
                                            else:
                                                amount += commission_lines.fixed_price
                                    if amount != 0:
                                        commission_line['amount'] = amount
                                        self.env['commission.line'].create(commission_line)
        pos = super(PosSession, self).action_pos_session_closing_control()
        return pos


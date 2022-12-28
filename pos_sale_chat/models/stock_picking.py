from odoo import models, _

class StockPicking(models.Model):
    _inherit = "stock.picking"

    def action_assign(self):
        rec = super(StockPicking, self).action_assign()
        if self.state == "assigned":
            partner_id = self.location_id.contact
            user_id = self.sale_id.user_id
            msg = _("Stock reservation successful!")
            subj = _("Stock reserve notification")
            self.message_post(body=msg)
            self.sale_id.send_chat(user_id, partner_id, msg, subj)
        else:
            self.message_post(body=_("Stock not available!"))
        return rec

    def get_url_stock_reserve(self):
        action_id = self.env.ref("pos_sale_chat.action_pos_reserve_products").id
        action = self.env['ir.actions.act_window'].browse(action_id)
        action.sudo().update({
            'domain': [('location_id', '=',self.location_id.id)]
        })
        url = "/web?#action=%s&model=%s&view_type=list" % (action_id, self._name)
        span = _("<a href='%s' target='_blank'>Committed products</a>") % url
        msg = _("You have committed products for sale Ecommerce %s") % (span)
        return msg

    def verify_stock_reserve(self):
        pickings = self.env["stock.picking"].search([("state","=","confirmed"),("company_id","=",self.env.company.id)])
        for pick in pickings:
            partner_id = pick.location_id.contact
            msg = pick.get_url_stock_reserve()
            pick.message_post(body=msg)
            pick.sale_id.send_notice(partner_id, msg)


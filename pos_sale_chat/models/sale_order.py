from odoo import models, _

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        rec = super(SaleOrder, self).action_confirm()
        for rec in self:
            if rec.picking_ids:
                for picking in rec.picking_ids:
                    if picking.state == 'confirmed':
                        partner_id = picking.location_id.contact
                        action_id = self.env.ref("pos_sale_chat.action_pos_reserve_products").id
                        action = self.env['ir.actions.act_window'].browse(action_id)
                        action.sudo().update({
                            'domain': [('location_id', '=',picking.location_id.id)]
                        })
                        url = "/web?#action=%s&model=%s&view_type=list" % (action_id, picking._name)
                        span = _("<a href='%s' target='_blank'>Committed products</a>") % url
                        rec.send_notice(partner_id, span)
        return rec

    def send_notice(self, partner_id, url):
        # notification_ids = [(0, 0, {
        #     'res_partner_id': 3,
        #     'notification_type': 'inbox'
        # })]
        # self.message_post(body='Probando si sale chat', message_type="notification", 
        #     subtype="mail.mt_comment", 
        #     author_id=self.user_id.partner_id.id, 
        #     notification_ids=notification_ids)
        
        channel_odoo_bot_users = '%s, %s' % (self.user_id.partner_id.name, partner_id.name)
        channel_obj = self.env['mail.channel']
        channel_id = channel_obj.search([('name', 'like', channel_odoo_bot_users)])
        if not channel_id:
            channel_id = channel_obj.create({
                'name': channel_odoo_bot_users,
                'email_send': False,
                'channel_type': 'chat',
                'public': 'private',
                'channel_partner_ids': [(4, self.user_id.partner_id.id),(4, partner_id.id)]
            })
        channel_id.message_post(
            subject=_("Stock reserve notification"),
            body=_("You have committed products for sale Ecommerce %s") % (url) ,
            message_type='comment',
            subtype='mail.mt_comment',
        )


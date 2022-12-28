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
                        msg = picking.get_url_stock_reserve()
                        rec.send_notice(partner_id, msg)
        return rec
    
    def send_notice(self, partner_id, msg):
        subj = _("Stock reserve notification")
        self.send_chat(self.user_id, partner_id, msg, subj)

    def send_chat(self, user_id, partner_id, message, subj):
        channel_odoo_bot_users = '%s, %s' % (user_id.partner_id.name, partner_id.name)
        channel_obj = self.env['mail.channel']
        channel_id = channel_obj.search([('name', 'like', channel_odoo_bot_users)])
        if not channel_id:
            channel_id = channel_obj.create({
                'name': channel_odoo_bot_users,
                'email_send': False,
                'channel_type': 'chat',
                'public': 'private',
                'channel_partner_ids': [(4, user_id.partner_id.id),(4, partner_id.id)]
            })
        channel_id.message_post(subject=subj, body=message, message_type='comment', subtype='mail.mt_comment')


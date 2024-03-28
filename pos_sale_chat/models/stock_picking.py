from odoo import models, _

class StockPicking(models.Model):
    _inherit = "stock.picking"

    def action_assign(self):
        rec = super(StockPicking, self).action_assign()

        for picking in self:
            if picking.sale_id.ma_order_id or picking.sale_id.meli_id:
                if picking.state == "assigned" or picking.state == "confirmed":
                    if picking.state == "assigned":
                        if picking.sale_id:
                            partner_id = picking.location_id.contact
                            user_id = picking.sale_id.user_id
                            msg = _("Review and reserve stock.")
                            subj = _("Stock reserve notification")
                            pick = picking
                            pick = pick.get_url_stock_reserve_custom()
                            picking.message_post(body=msg)
                            picking.sale_id.send_chat(user_id, partner_id, pick, subj)
                            msg = _("Reservation made.")
                            subj = _("Stock reserve notification")
                            for product in picking.product_id:
                                product.GtExportSingleProductStock()
                            picking.message_post(body=msg)
                else:
                    picking.message_post(body=_("Stock not available!"))
                
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


    def get_url_stock_reserve_custom(self):
        action_id = self.env.ref("pos_sale_chat.action_pos_reserve_products").id
        active_id = self.env['ir.actions.act_window'].browse(action_id)
        cids = self.env.company.id
        record_id = self.id
        menu_id = 735
        model = 'stock.picking'
        
        # Construir el primer enlace específico
        url_specific = "/web#action=1149&active_id=ir.actions.act_window(1149%2C)&model=stock.picking&view_type=list&cids=2&menu_id=735"
        
        # Construir la URL con los parámetros especificados por la función
        url_custom = "/web#action={action_id}&active_id={active_id}&cids={cids}&id={record_id}&menu_id={menu_id}&model={model}&view_type=form".format(
            action_id=action_id,
            active_id=active_id.id,  # Se asume que active_id es un registro y se necesita su ID
            cids=cids,
            record_id=record_id,
            menu_id=menu_id,
            model=model
        )
        
        # Crear los enlaces HTML
        link_specific = "<a href='{url}' target='_blank'>Specific Link</a>".format(url=url_specific)
        link_custom = "<a href='{url}' target='_blank'>Commited Products</a>".format(url=url_custom)
        
        # Crear el mensaje con ambos enlaces
        msg = "You have deliveries to confirm: {link_specific} and {link_custom}".format(link_specific=link_specific, link_custom=link_custom)
        return msg

    def verify_stock_reserve(self):
        pickings = self.env["stock.picking"].search([("state","=","confirmed"),("company_id","=",self.env.company.id),("sale_id","!=", False)])
        for pick in pickings:
            partner_id = pick.location_id.contact
            msg = pick.get_url_stock_reserve()
            pick.message_post(body=msg)
            pick.sale_id.send_notice(partner_id, msg)


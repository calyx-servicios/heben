from odoo import fields, models, _
from datetime import date

import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    def cron_automation_ecommerce_sales(self):
        ma_obj = self.env["mail.activity"]
        act_type = self.env.ref("mail.mail_activity_data_warning").id
        model_sale = self.env.ref("sale.model_sale_order")
        user_act = self.env.ref("automation_ecommerce_sales.user_automation_ecommerce").id
        vals = {
            "activity_type_id": act_type,
            "date_deadline": date.today(),
            "summary": _("Automation Ecommerce Sales"),
            "user_id": user_act,
            "res_model_id": model_sale.id,
            "res_model": model_sale.model
        }
        #Ordenes de magento
        orders = self.env["sale.order"].search([('ma_order_id','!=',''),('order_status','=','processing')])
        for order in orders:
            try:
                order.check_location()
                try:
                    order.action_confirm()
                    try:
                        order._create_invoices()
                    except:
                        msg = _('Error creating the invoice for the sale ') + order.name
                        vals.update({"note": msg, "res_id": order.id, "res_name": order.name})
                        ma_except = ma_obj.create(vals)
                        ma_except.action_close_dialog()
                except:
                    msg = _('Error confirming sales order ') + order.name
                    vals.update({"note": msg, "res_id": order.id, "res_name": order.name})
                    ma_except = ma_obj.create(vals)
                    ma_except.action_close_dialog()
            except:
                msg = _('For the sale order ') + order.name  + _(' there is no stock in the selected locations.')
                vals.update({"note": msg, "res_id": order.id, "res_name": order.name})
                ma_except = ma_obj.create(vals)
                ma_except.action_close_dialog()
        
        #Ordenes de mercado libre
        try:
            settings_instance = self.env["melisync.settings"].search([], limit=1)
            if settings_instance:
                self.env["sale.order"].meli_get_sales(settings_instance)
                meli_orders = self.env["sale.order"].search([('meli_id', '!=', ""),('state','in', ['draft','sent'])])
                if meli_orders:
                    for meli_order in meli_orders:
                        try:
                            meli_order.action_confirm()
                        except:
                            msg = _('Error confirming sales order ') + meli_order.name
                            vals.update({"note": msg, "res_id": meli_order.id, "res_name": meli_order.name})
                            ma_except = ma_obj.create(vals)
                            ma_except.action_close_dialog()
        except ValueError as e:
            _logger.info(e)


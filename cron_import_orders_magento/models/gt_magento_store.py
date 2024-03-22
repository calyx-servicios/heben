from odoo import models
from logging import Logger

class GTMagentoStore(models.Model):
    _inherit = "gt.magento.store"

    def import_ar_orders(self):
        rec = self.env['gt.magento.store'].search(['|', ('name', '=', 'Heben AR View'), ('code', '=', 'default2')], limit=1)
        if rec:
            rec.GtCreateMagentoOrders()

    def import_cl_orders(self):
        rec = self.env['gt.magento.store'].search(['|', ('name', '=', 'Heben CL View'), ('code', '=', 'default1')], limit=1)
        if rec:
            rec.GtCreateMagentoOrders()
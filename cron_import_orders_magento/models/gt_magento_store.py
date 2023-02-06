from odoo import models

class GTMagentoStore(models.Model):
    _inherit = "gt.magento.store"

    def import_ar_orders(self):
        self.env['gt.magento.store'].search([('name','=','Heben AR View')]).GtCreateMagentoOrders()

    def import_cl_orders(self):
        self.env['gt.magento.store'].search([('name','=','Heben CL View')]).GtCreateMagentoOrders()
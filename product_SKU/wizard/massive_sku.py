# -*- coding: utf-8 -*-
from odoo import fields, models, _

class MassiveSkuWizard(models.TransientModel):
    _name = "massive.sku.wizard"
    _description = _("Create SKU for products")
    
    use_sku = fields.Boolean("Use sku?", default=False)
    mask_sku_id = fields.Many2one('mask.sku', string="Internal Reference", help="Select a rule sku for this product")
    
    def massive_sku(self):
        prod_obj = self.env['product.product']
        active_ids = self.env.context.get('active_ids')
        if len(active_ids) != 0:
            product_ids = prod_obj.browse(active_ids)
            product_ids.write({"use_sku": self.use_sku, "mask_sku_id": self.mask_sku_id.id})
            for product in product_ids:
                product.onchage_mask_sku_id()
    
    def massive_sku_template(self):
        prod_obj = self.env['product.template']
        active_ids = self.env.context.get('active_ids')
        if len(active_ids) != 0:
            product_ids = prod_obj.browse(active_ids)
            product_ids.write({"use_sku": self.use_sku, "mask_sku_id": self.mask_sku_id.id})
            for product in product_ids:
                product.onchage_mask_sku_id()
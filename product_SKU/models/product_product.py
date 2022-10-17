from odoo import models, fields, api

class ProductProduct (models.Model):
    _inherit = 'product.product'

    mask_sku_id = fields.Many2one('mask.sku',string="Internal Reference", help="Select a rule sku for this product")
    use_sku = fields.Boolean()

    @api.onchange('mask_sku_id')
    def onchage_mask_sku_id(self):
        if self.mask_sku_id:
            code_list = self.mask_sku_id.code_list.split(',')
            sku_fields = {'-':'-'}
            if self.product_seasons_id:
                sku_fields['product_seasons_id'] = self.product_seasons_id.code
            if self.product_family_id:
                sku_fields['product_family_id'] = self.product_family_id.code
            if self.product_material_id:
                sku_fields['product_material_id'] = self.product_material_id.code
            variant_color_id = self.product_template_attribute_value_ids.filtered(lambda attribute: attribute.display_type == 'color')
            if len(variant_color_id) >= 1:
                sku_fields['variant_color_id'] = variant_color_id[0].product_attribute_value_id.code
            variant_talle_id = self.product_template_attribute_value_ids.filtered(lambda attribute: attribute.display_type == 'talle')
            if len(variant_talle_id) >= 1:
                sku_fields['variant_talle_id'] = variant_talle_id[0].product_attribute_value_id.code
            if len(self.variant_seller_ids) >= 1:
                sku_fields['partner_code'] = self.variant_seller_ids[0].name.partner_code
            if self.internal_code:
                sku_fields['internal_code'] = self.internal_code
            sku = ''
            for code in code_list:
                    sku += sku_fields.get(code,'')
            self.default_code = sku
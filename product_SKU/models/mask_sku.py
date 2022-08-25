from odoo import models, fields, api, _

class MaskSku(models.Model):
    _name = "mask.sku"
    _description = "Mask Sku"

    name = fields.Char(required=True)

    sku_rules_ids = fields.One2many('sku.rule','mask_sku_id')
    sku_example = fields.Char()
    code_list = fields.Char()

    @api.onchange("sku_rules_ids")
    def onchange_code_list(self):
        sku_name = []
        product = self.env['product.product'].search([('use_sku','=',True)],limit=1)
        for rule in self.sku_rules_ids:
            if rule.rule_id.name and rule.rule_id.field_require_rule != 'separator':
                sku_name.append(rule.rule_id.field_require_rule)
            else:
                sku_name.append('-')
        if len(sku_name) >= 1:
            self.code_list = ','.join(sku_name)
        
        if product.mask_sku_id:
            sku_fields = {}
            if product.product_seasons_id:
                sku_fields['product_seasons_id'] = product.product_seasons_id.code
            if product.product_family_id:
                sku_fields['product_family_id'] = product.product_family_id.code
            if product.product_material_id:
                sku_fields['product_material_id'] = product.product_material_id.code
            variant_color_id = product.product_template_attribute_value_ids.filtered(lambda attribute: attribute.display_type == 'color')
            if len(variant_color_id) >= 1:
                sku_fields['variant_color_id'] = variant_color_id[0].product_attribute_value_id.code
            variant_talle_id = product.product_template_attribute_value_ids.filtered(lambda attribute: attribute.display_type == 'talle')
            if len(variant_talle_id) >= 1:
                sku_fields['variant_talle_id'] = variant_talle_id[0].product_attribute_value_id.code
            if len(product.variant_seller_ids) >= 1:
                sku_fields['partner_code'] = product.variant_seller_ids[0].name.partner_code
            if product.internal_code:
                sku_fields['internal_code'] = product.internal_code
            sku = ''
            for code in sku_name:
                if code == '-':
                    sku += code
                else:
                    sku += sku_fields.get(code,'')
            self.sku_example = sku
from odoo import models, _
from odoo.exceptions import AccessError

class ProductProduct(models.Model):
    _inherit = "product.product"

    def magento_product_export(self):
        if not self.env.user.has_group('globalteckz_magento_2.group_magento_manager'):
            raise AccessError(_("You don't have the necessary permissions to perform this action."))

        data = []
        for product in self:
            vals = {
                'sku': product.default_code or '',
                'name': product.name,
                'description': product.description or '',
                'price': product.lst_price,
                'stock': product.qty_available,
                'ds_category': product.categ_id.display_name,
                'ds_material_filter': product.product_material_id.name,
                'meta_description': product.description or '',
            }
            for attrs in product.product_template_attribute_value_ids:
                if attrs.display_type == 'color':
                    if vals.get('ds_color_filter'):
                        vals['ds_color_filter'] += attrs.name
                    else:
                        vals['ds_color_filter'] = attrs.name
            data.append(vals)
        data_export = {
            'data': data,
        }
        return self.env.ref('magento_product_export.product_export_xls').report_action(self, data=data_export)


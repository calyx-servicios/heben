from odoo import models, _
from odoo.exceptions import AccessError, UserError

class ProductProduct(models.Model):
    _inherit = "product.product"

    ATTRIBUTE_FIELD_MAPPING = {
        'ds_color_filter': 'ds_color_filter',
        'ds_material_filter': 'ds_material_filter',
    }

    def _check_magento_manager_permission(self):
        if not self.env.user.has_group('globalteckz_magento_2.group_magento_manager'):
            raise AccessError(_("You don't have the necessary permissions to perform this action."))

    def _prepare_magento_product_data(self, product):
        if not product.description:
            raise UserError(_('To export to Magento, the description field is required'))

        ds_category = product.prod_attr_category_id.label
        if not ds_category:
            raise UserError(_('The product {} does not have ds_category'.format(product.name)))

        vals = {
            'sku': product.default_code or '',
            'name': product.name,
            'description': product.description,
            'price': product.lst_price,
            'stock': product.qty_available,
            'meta_description': product.description,
            'ds_category': ds_category,
        }

        return vals

    def magento_product_export(self):
        self._check_magento_manager_permission()

        data = []
        for product in self:
            vals = self._prepare_magento_product_data(product)

            attributes_magento = product.product_template_attribute_value_ids.filtered(lambda x: x.attribute_id.is_attribute_magento)
            if attributes_magento:
                # Attributes exported from Magento
                for attrs in attributes_magento:
                    attr_magento = self.env['gt.product.attributes'].search([('magento_id', '=', attrs.attribute_id.attribute_magento_id)])
                    attribute_code = attr_magento.attribute_code
                    field_name = self.ATTRIBUTE_FIELD_MAPPING.get(attribute_code)
                    if field_name:
                        vals[field_name] = vals.get(field_name, '') + attrs.name
            else:
                # Attributes from Odoo
                if not product.product_material_id.name:
                    raise UserError(_('The product {} does not have ds_material_filter'.format(product.name)))
                for attrs in product.product_template_attribute_value_ids:
                    if attrs.display_type == 'color':
                        if vals.get('ds_color_filter'):
                            vals['ds_color_filter'] += attrs.name
                        else:
                            vals['ds_color_filter'] = attrs.name

            data.append(vals)

        data_export = {'data': data}
        return self.env.ref('magento_product_export.product_export_xls').report_action(self, data=data_export)

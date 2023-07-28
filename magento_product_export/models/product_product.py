from odoo import models, _
from odoo.exceptions import AccessError, UserError

class ProductProduct(models.Model):
    _inherit = "product.product"

    ATTRIBUTE_FIELD_MAPPING = {
        'ds_color_filter': 'ds_color_filter',
        'ds_material_filter': 'ds_material_filter',
        'ds_category': 'ds_category',
    }

    def _check_magento_manager_permission(self):
        if not self.env.user.has_group('globalteckz_magento_2.group_magento_manager'):
            raise AccessError(_("You don't have the necessary permissions to perform this action."))

    def _prepare_magento_product_data(self, product):
        if not product.description:
            raise UserError(_('To export to Magento, the description field is required'))

        vals = {
            'sku': product.default_code or '',
            'name': product.name,
            'description': product.description,
            'price': product.lst_price,
            'stock': product.qty_available,
            'meta_description': product.description,
        }

        return vals

    def magento_product_export(self):
        self._check_magento_manager_permission()

        data = []
        for product in self:
            vals = self._prepare_magento_product_data(product)

            attributes_magento = product.product_template_attribute_value_ids.filtered(lambda x: x.attribute_id.is_attribute_magento)
            if not attributes_magento:
                raise UserError(_('The product {} has no Magento attributes'.format(product.name)))

            for attrs in attributes_magento:
                attr_magento = self.env['gt.product.attributes'].search([('magento_id', '=', attrs.attribute_id.attribute_magento_id)])
                attribute_code = attr_magento.attribute_code
                field_name = self.ATTRIBUTE_FIELD_MAPPING.get(attribute_code)
                if field_name:
                    vals[field_name] = vals.get(field_name, '') + attrs.name

            data.append(vals)

        data_export = {'data': data}
        return self.env.ref('magento_product_export.product_export_xls').report_action(self, data=data_export)

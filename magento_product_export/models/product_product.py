from odoo import models, _
from odoo.exceptions import AccessError, UserError
import re

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

        if "simple" in product.product_type:
            visibility = "Not Visible Individually"
        if "configurable" in product.product_type:
            visibility = "Catalog, Search"

        sitiosWeb= product.website_ids
        website = []
        for sitio in sitiosWeb:
            if sitio.code:
                website.append(sitio.code)
        websiteConcat = ', '.join(website)
        
        urlKey = str(product.default_code).lower()
        
        vals = {
            'sku': product.default_code or '',
            'attribute_set_code':product.attribute_set.display_name,
            'product_type':product.product_type,
            'product_websites': websiteConcat,#product.website_ids,
            'name': product.name,
            'weight': '0.2',
            'description': product.description,
            'price': product.lst_price,
            'tax_class_name':'Taxable Goods',
            'visibility':visibility,
            'url_key':urlKey,
            'stock': product.qty_available,
            'meta_description': product.description,
            'ds_category': ds_category,
            'product_online': 1,
            'color': str(product.default_code[-6:-3]),
            'size':str(product.default_code[-3:]),
            'model_code':str(product.default_code[4:8]),
            'color_code':str(product.default_code[-6:-3]),
            'auto_relate':'YES',
            'ds_family':str(product.default_code[0:1]),
            'ds_provider':str(product.default_code[1:3]),
            'ds_season':str(product.default_code[8:10]),
            'qty': product.qty_available,
            'use_config_min_qty':1,
            'use_config_max_sale_qty':1,
            'is_in_stock':1,
            'use_config_notify_stock_qty':1,
            'manage_stock por defecto':1,
            'use_config_manage_stock':1,
            'website_id':0,
            'configurable_product_name': product.product_tmpl_id.display_name,
            'configurable_product_type':'configurable',
            'configurable_product_sku': product.product_tmpl_id.magento_sku,
            'configurable_visibility': 'Catalog, Search',
            'configurable_color': '',
            'configurable_url_key': str(product.product_tmpl_id.magento_sku).lower(),
        }

        return vals

    def magento_product_export(self):
        self._check_magento_manager_permission()

        data = []
        for product in self:
            vals = self._prepare_magento_product_data(product)

            vals['ds_color_filter'] = ''
            vals['ds_material_filter'] = product.product_material_id.name if product.product_material_id.name else ''
            vals['ds_material'] = vals['ds_material_filter'][0:2]
            vals['ds_material_filter'] = vals['ds_material_filter'][3:]
    
            attributes_magento = product.product_template_attribute_value_ids

            for attribute in attributes_magento:
                display_type = attribute['display_type']
                if 'color' == display_type:
                    vals['ds_color_filter'] = str(attribute['name']).lower()     

            data.append(vals)

        data_export = {'data': data}
        return self.env.ref('magento_product_export.product_export_xls').report_action(self, data=data_export)
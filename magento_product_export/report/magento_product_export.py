from odoo import models, _
import xlsxwriter


class MagentoProductExportXls(models.AbstractModel):
    _name = "report.magento_product_export.product_export_xls"
    _inherit = "report.report_xlsx.abstract"
    _description = "Magento Product Export Xls"


    def generate_xlsx_report(self, workbook, data, obj):
        # Set delimiter
        workbook.delimiter = ';'
        sheet = workbook.add_worksheet(_('Product Report'))
        bold = workbook.add_format({'bold': True, 'align': 'center'})

        # Prepare Headers and width
        columns = [
            ('A', 24, 'sku'),
            ('B', 18, 'attribute_set_code'),
            ('C', 18, 'product_type'),
            ('D', 18, 'product_websites'),
            ('E', 18, 'name'),
            ('F', 18, 'description'),
            ('G', 18, 'weight'),
            ('H', 18, 'product_online'),
            ('I', 18, 'tax_class_name'),
            ('J', 18, 'visibility'),
            ('K', 18, 'price'),
            ('L', 18, 'url_key'),
            ('M', 18, 'meta_description'),
            ('N', 18, 'stock'),
            ('O', 18, 'color'),
            ('P', 18, 'size'),
            ('Q', 18, 'color_code'),
            ('R', 18, 'model_code'),
            ('S', 18, 'auto_relate'),
            ('T', 18, 'ds_material'),
            ('U', 18, 'ds_family'),
            ('V', 18, 'ds_provider'),
            ('W', 18, 'ds_color_filter'),
            ('X', 18, 'ds_season'),
            ('Y', 18, 'ds_material_filter'),
            ('Z', 18, 'ds_category'),
            ('AA', 18, 'qty'),
            ('AB', 18, 'use_config_min_qty'),
            ('AC', 18, 'use_config_max_sale_qty'),
            ('AD', 18, 'is_in_stock'),
            ('AE', 18, 'use_config_notify_stock_qty'),
            ('AF', 18, 'manage_stock',),
            ('AG', 18, 'use_config_manage_stock'),
            ('AH', 18, 'website_id'),
            ('AI', 18, 'configurable_variations'),
        ]

        # Creating column headers
        for col, width, label in columns:
            sheet.set_column(f'{col}:{col}', width)
            sheet.write(f'{col}1', label, bold)

        # Row after header
        row = 1
        
        name_products_configurables = []
        conf_variations_txt = ""
        conf_variations = []
        last_data = {
            'name':''
        }

        # Setting values on cells
        for product_data in data['data']:
            formatted_price = '{:.2f}'.format(float(product_data.get('price', 0.0))).replace(',', '.')
            if product_data['configurable_product_name'] not in name_products_configurables:
                
                if (last_data['name'] != product_data['configurable_product_name']) and (last_data['name'] != ''):
                    data_configurable = "|".join(conf_variations)
                    row_data = [
                    configurables['product_sku'],
                    last_data.get('attribute_set_code', ''),
                    configurables['product_type'],
                    last_data.get('product_websites', ''),
                    configurables['name'],
                    last_data.get('description', ''),
                    last_data.get('weight', ''),
                    last_data.get('product_online', ''),
                    last_data.get('tax_class_name', ''),
                    configurables['visibility'],
                    last_formatted_price,
                    configurables['url_key'],
                    last_data.get('meta_description', ''),
                    last_data.get('stock', 0),
                    configurables['color'],
                    configurables['size' ],
                    last_data.get('color_code', ''),
                    last_data.get('model_code', ''),
                    last_data.get('auto_relate', ''),
                    last_data.get('ds_material', ''),
                    last_data.get('ds_family', ''),
                    last_data.get('ds_provider', ''),
                    last_data.get('ds_color_filter', ''),
                    last_data.get('ds_season', ''),
                    last_data.get('ds_material_filter', ''),
                    last_data.get('ds_category', ''),
                    last_data.get('qty', ''),
                    last_data.get('use_config_min_qty', ''),
                    last_data.get('use_config_max_sale_qty', ''),
                    last_data.get('is_in_stock', ''),
                    last_data.get('use_config_notify_stock_qty', ''),
                    last_data.get('manage_stock', ''),
                    last_data.get('use_config_manage_stock', ''),
                    last_data.get('website_id', ''),
                    data_configurable,
                    ]
                    name_products_configurables.append(configurables['name'])
                    sheet.write_row(row, 0, row_data)
                    row += 1
                    data_configurable = ""
                    conf_variations = []
                    conf_variations_txt = ""


                configurables ={ 'name':product_data['configurable_product_name'],
                     'product_type': product_data['configurable_product_type'],
                     'product_sku': product_data['configurable_product_sku'],
                     'visibility': product_data['configurable_visibility'],
                     'color': product_data['configurable_color'],
                     'url_key': product_data['configurable_url_key'],
                     'size': '',
                     }
                name_products_configurables.append(configurables['name'])

                last_configurable_product = product_data['configurable_product_name']

            if (product_data['product_type'] == 'simple'):
                row_data = [
                    product_data.get('sku', ''),
                    product_data.get('attribute_set_code', ''),
                    product_data.get('product_type', ''),
                    product_data.get('product_websites', ''),
                    product_data.get('name', ''),
                    product_data.get('description', ''),
                    product_data.get('weight', ''),
                    product_data.get('product_online', ''),
                    product_data.get('tax_class_name', ''),
                    product_data.get('visibility', ''),
                    formatted_price,
                    product_data.get('url_key', ''),
                    product_data.get('meta_description', ''),
                    product_data.get('stock', 0),
                    product_data.get('color', ''),
                    product_data.get('size', ''),
                    product_data.get('color_code', ''),
                    product_data.get('model_code', ''),
                    product_data.get('auto_relate', ''),
                    product_data.get('ds_material', ''),
                    product_data.get('ds_family', ''),
                    product_data.get('ds_provider', ''),
                    product_data.get('ds_color_filter', ''),
                    product_data.get('ds_season', ''),
                    product_data.get('ds_material_filter', ''),
                    product_data.get('ds_category', ''),
                    product_data.get('qty', ''),
                    product_data.get('use_config_min_qty', ''),
                    product_data.get('use_config_max_sale_qty', ''),
                    product_data.get('is_in_stock', ''),
                    product_data.get('use_config_notify_stock_qty', ''),
                    product_data.get('manage_stock', ''),
                    product_data.get('use_config_manage_stock', ''),
                    product_data.get('website_id', ''),
                ]
            
                conf_variations_txt = f"sku={product_data['sku']},color={product_data['color']},size={product_data['size']}"
                conf_variations.append(conf_variations_txt)

            last_data = product_data
            last_formatted_price = formatted_price
            sheet.write_row(row, 0, row_data)
            row += 1

        if last_data['name']:
            data_configurable = "|".join(conf_variations)
            row_data = [
                    configurables['product_sku'],
                    last_data.get('attribute_set_code', ''),
                    configurables['product_type'],
                    last_data.get('product_websites', ''),
                    configurables['name'],
                    last_data.get('description', ''),
                    last_data.get('weight', ''),
                    last_data.get('product_online', ''),
                    last_data.get('tax_class_name', ''),
                    configurables['visibility'],
                    last_formatted_price,
                    configurables['url_key'],
                    last_data.get('meta_description', ''),
                    last_data.get('stock', 0),
                    configurables['color'],
                    configurables['size'],
                    last_data.get('color_code', ''),
                    last_data.get('model_code', ''),
                    last_data.get('auto_relate', ''),
                    last_data.get('ds_material', ''),
                    last_data.get('ds_family', ''),
                    last_data.get('ds_provider', ''),
                    last_data.get('ds_color_filter', ''),
                    last_data.get('ds_season', ''),
                    last_data.get('ds_material_filter', ''),
                    last_data.get('ds_category', ''),
                    last_data.get('qty', ''),
                    last_data.get('use_config_min_qty', ''),
                    last_data.get('use_config_max_sale_qty', ''),
                    last_data.get('is_in_stock', ''),
                    last_data.get('use_config_notify_stock_qty', ''),
                    last_data.get('manage_stock', ''),
                    last_data.get('use_config_manage_stock', ''),
                    last_data.get('website_id', ''),
                    data_configurable,
                ]
        sheet.write_row(row, 0, row_data)
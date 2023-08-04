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
            ('A', 50, 'sku'),
            ('B', 18, 'name'),
            ('C', 18, 'description'),
            ('D', 18, 'price'),
            ('E', 18, 'stock'),
            ('F', 18, 'ds_category'),
            ('G', 18, 'ds_material_filter'),
            ('H', 18, 'ds_color_filter'),
            ('I', 18, 'meta_description'),
        ]

        # Creating column headers
        for col, width, label in columns:
            sheet.set_column(f'{col}:{col}', width)
            sheet.write(f'{col}1', label, bold)

        # Row after header
        row = 1

        # Setting values on cells
        for product_data in data['data']:
            formatted_price = '{:.2f}'.format(float(product_data.get('price', 0.0))).replace(',', '.')

            row_data = [
                product_data.get('sku', ''),
                product_data.get('name', ''),
                product_data.get('description', ''),
                formatted_price,
                product_data.get('stock', 0),
                product_data.get('ds_category', ''),
                product_data.get('ds_material_filter', ''),
                product_data.get('ds_color_filter', ''),
                product_data.get('meta_description', ''),
            ]
            sheet.write_row(row, 0, row_data)
            row += 1

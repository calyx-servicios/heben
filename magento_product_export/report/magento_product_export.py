from odoo import models, _
import xlsxwriter
from odoo.exceptions import AccessError

class MagentoProductExportXls(models.AbstractModel):
    _name = "report.magento_product_export.product_export_xls"
    _inherit = "report.report_xlsx.abstract"
    _description = "Magento Product Export Xls"

    def generate_xlsx_report(self, workbook, data, obj):
        sheet = workbook.add_worksheet(_('Product Report'))
        bold = workbook.add_format({
            'bold': True,
            'align': 'center'
        })
        price_format = workbook.add_format({'num_format': '#,##0.00'})
        price_format.set_num_format('#,##0.00')

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

        for col, width, label in columns:
            sheet.set_column(f'{col}:{col}', width)
            sheet.write(f'{col}1', label, bold)

        row = 2

        for product_data in data['data']:
            sheet.write(f'A{row}', product_data['sku'])
            sheet.write(f'B{row}', product_data['name'])
            sheet.write(f'C{row}', product_data['description'])
            sheet.write(f'D{row}', product_data['price'], price_format)
            sheet.write(f'E{row}', product_data['stock'])
            sheet.write(f'F{row}', product_data['ds_category'])
            sheet.write(f'G{row}', product_data['ds_material_filter'])
            sheet.write(f'H{row}', product_data['ds_color_filter'])
            sheet.write(f'I{row}', product_data['meta_description'])

            row += 1

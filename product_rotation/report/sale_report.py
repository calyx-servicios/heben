from odoo import models,fields,api,_

class SaleReport(models.Model):
    _inherit = "sale.report"

    product_color = fields.Many2one(string='Color', comodel_name='product.template.attribute.value')

    product_name_and_color = fields.Char(string='product_name_and_color')

    location_id = fields.Many2one(comodel_name='stock.location',string= 'Stock Location', readonly=True)

    qty_available = fields.Float(string='Available Quantity', readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        #add product_color to rows and columns
        fields['product_color'] = ", p.product_color as product_color"
        groupby += ', p.product_color'
        fields['product_name_and_color'] = ", p.product_name_and_color as product_name_and_color"
        groupby += ', p.product_name_and_color'
        #add location_id to rows and columns
        fields['location_id'] = ", l.location_id as location_id"
        groupby += ', l.location_id'
        #add qty_available to measures
        fields['qty_available'] = ", sum(p.qty_available) as qty_available"
        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)
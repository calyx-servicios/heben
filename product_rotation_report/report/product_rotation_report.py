from odoo import models, fields, api, _
from odoo import tools
from datetime import datetime
from dateutil.relativedelta import relativedelta

class ProductRotationReport(models.Model):
    _name = 'product.rotation.report'
    _description = 'Product Rotation Data for Report'
    _auto = False

    partner_id = fields.Many2one('res.partner', string="Partner Company")
    company_id = fields.Many2one('res.company', string="Company")
    product_id = fields.Many2one('product.product', string="Product")
    product_and_color = fields.Char(string="Product + Color")
    product_color = fields.Char(string="Color")
    product_size = fields.Char(string="Size")
    product_template_id = fields.Many2one('product.template', string="Product Template")
    categ_id = fields.Many2one('product.category', string="Category")
    brand_id = fields.Many2one('product.brand', string="Brand")
    product_season_id = fields.Many2one('product.seasons', string="Season")
    product_family_id = fields.Many2one('product.family', string="Product Family")
    product_material_id = fields.Many2one('product.material', string="Product Material")
    location_id = fields.Many2one('stock.location', string="Stock Location")
    date_order = fields.Date(string="Date")
    available = fields.Float(string="Available")
    sold = fields.Float(string="Sold")

    def init(self):
        vdate_from = self.env.context.get('date_from', datetime.today().date())
        vdate_to = self.env.context.get('date_to', datetime.today().date())

        tools.drop_view_if_exists(self._cr, 'product_rotation_report')
        self._cr.execute(""" CREATE OR REPLACE VIEW product_rotation_report AS (
                    select id
                         , partner_id
                         , company_id
                         , product_id
                         , product_and_color
                         , product_color
                         , product_size
                         , product_template_id
                         , categ_id
                         , brand_id
                         , product_season_id
                         , product_family_id
                         , product_material_id
                         , product_material
                         , location_id
                         , date_order
                         , available
                         , sold
                      from product_rotation_report() as (id integer, partner_id integer, company_id integer, company varchar, default_code varchar, product_id integer, product_and_color varchar,
			 product_color varchar, product_size varchar, product_template_id integer, categ_id integer, categ varchar, brand_id integer, brand varchar, product_season_id integer, 
			 product_season varchar, product_family_id integer,product_family varchar, product_material_id integer, product_material varchar, 
			 location_id integer, location_name varchar, date_order date, available decimal(12,2), sold decimal(12,2)))""",(vdate_from, vdate_to))


class ReportRotationWizard(models.TransientModel):
    _name = 'product.rotation.report.wizard'
    _description = 'Product Rotation Wizard for Report'

    date_from = fields.Date(default=datetime.today() - relativedelta(month=1,day=1),required=True, string="Desde")
    date_to = fields.Date(default=fields.Date.context_today, required=True, string="Hasta")

    def action_confirm(self):
        ctx = self.env.context.copy()
        ctx.update({'date_from': self.date_from, 'date_to': self.date_to})

        self.env['product.rotation.report'].with_context(ctx).init()

        return {'name': "Product Rotation Report",
                'type': 'ir.actions.act_window',
                'res_model': 'product.rotation.report',
                'view_mode': 'pivot,tree',
                'view_type': 'form',
                'context': ctx,
            }

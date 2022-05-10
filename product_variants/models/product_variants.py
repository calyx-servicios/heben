from odoo import models, fields
import datetime
import time

class ProductProduct (models.Model):
    _inherit = 'product.product'

    
    discharge_date = fields.Char(string="Discharge date", compute="_compute_discharge_date")
    first_entry_date = fields.Char(string="First Entry Date", compute="_compute_date_first_entry")
    first_sale_date = fields.Char(string="First Sale Date", compute="_compute_date_firts_sale")
    last_entry_date = fields.Char(string="Last Entry Date", compute="_compute_date_last_entry")
    last_sale_date = fields.Char(string="Last Sale Date", compute="_compute_date_last_sale")

    def _compute_date_first_entry(self):
        record = self.env['stock.move.line'].search([('product_id', '=', self.id),('picking_code', '=', 'incoming'),('state', '=', 'done')], order='date asc', limit=1)
        if record.date:
            self.first_entry_date = str(record.date)[:11]
        else:
            self.first_entry_date = ""

    def _compute_date_firts_sale(self):
        record = self.env['stock.move.line'].search([('product_id', '=', self.id),('picking_code', '=', 'outgoing'),('state', '=', 'done'),('origin', '!=', False)], order='date asc', limit=1)
        if record.date:
            self.first_sale_date = str(record.date)[:11]
        else:
            self.first_sale_date = ""

    def _compute_date_last_sale(self):
        record = self.env['stock.move.line'].search([('product_id', '=', self.id),('picking_code', '=', 'outgoing'),('state', '=', 'done'),('origin', '!=', False)], order='date desc', limit=1)
        if record.date:
            self.last_sale_date = str(record.date)[:11]
        else:
            self.last_sale_date = ""

    def _compute_date_last_entry(self):
        record = self.env['stock.move.line'].search([('product_id', '=', self.id),('picking_code', '=', 'incoming'),('state', '=', 'done')], order='date desc', limit=1)
        if record.date:
            self.last_entry_date = str(record.date)[:11]
        else: 
            self.last_entry_date = ""

    def _compute_discharge_date(self):
        
        if self.create_date:
            self.discharge_date = str(self.create_date)[:11]
        else: 
            self.discharge_date = ""
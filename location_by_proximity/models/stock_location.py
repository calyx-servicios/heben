from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import re


class StockLocation(models.Model):
    _inherit = "stock.location"
    _order = "sequence"

    name = fields.Char(required=False)
    contact = fields.Many2one("res.partner")
    zip_code_field = fields.Char("Postal Code")
    zip_interval = fields.Char("Zip Interval")
    zip_code = fields.Integer("Zip")
    location_id = fields.Many2one("stock.location")
    secondary_location_ids = fields.Many2many(
        "stock.location", "rel_secondary_location", "location", "location_ids"
    )
    sequence = fields.Integer()

    def search_by_zip(self, zip_code):
        matched_locations = self.env["stock.location"]

        for location in self.env["stock.location"].search([]):
            if location.zip_interval:
                interval = re.sub(r"[^\d,\s-]", "", location.zip_interval)
                interval = re.sub(r"\s+", "", interval)
                intervals = [
                    tuple(map(int, interval.split("-")))
                    for interval in location.interval.split(",")
                ]
                if any(start <= zip_code <= end for start, end in intervals):
                    matched_locations += location

        return matched_locations

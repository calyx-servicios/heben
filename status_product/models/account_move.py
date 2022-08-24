from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    product_id = fields.Many2one('product.product')


from odoo import models,api,fields, _
from datetime import date
import re
import base64

class StockPicking(models.Model):
    _inherit = 'stock.picking'


    in_branch = fields.Selection([('in_branch','In Branch'),
            ('in_address','In Address'),],string="Delivery type")

    branch_post_id = fields.Many2one('stock.post.branch',string='Branch Post')



    def create_template_label_in_branch(self):
        return self.env.ref('label_argentine_post.action_report_preprinted_label_in_branch').report_action(self)

    def create_template_label_in_address(self):
        return self.env.ref('label_argentine_post.action_report_preprinted_label_in_address').report_action(self)
    


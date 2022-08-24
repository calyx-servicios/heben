from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ProductStatus(models.Model):
    _inherit = 'product.product'

    @api.model
    def create(self, vals_list):
        #Attempt to set a default image in the product.
        #recs.config_logo = recs._get_image()
        return super(ProductStatus, self).create(vals_list) 
    
    state = fields.Selection([
            ('active','Active'),
            ('in_out','In-Out'),
            ('liquidation','Liquidation'),
            ('low','Low'),
            ('draft', 'Draft'),
            ],'State', index=True, default='draft', track_visibility='allways',
            help="Commercial treatment status\n"
             " * Active: Most of the articles will have this status, it indicates that the product can be bought, sold and distributed freely.\n"
             " * In-Out: Indicates that you should not continue buying. That is bought only once, but it is not continuous.\n"
             " * Liquidation: It tells us that no replacements or purchases should be made. When its stock is finished, the product will be canceled and will not re-enter.\n"
             " * Low: The product will no longer be marketed in the company. Block the sale, purchase and distribution, the stock must be at 0.\n")

    @api.onchange("state")
    def _onchange_state(self):
        for record in self:
            if record.state == "low" and record.qty_available:
                raise ValidationError(_("The stock must be at 0"))


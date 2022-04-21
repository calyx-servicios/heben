from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ProductStatus (models.Model):
    _inherit = 'product.product'

    
    @api.model
    def create(self):
        recs.config_logo = recs._get_image()
    
    state = fields.Selection([
            ('active','Active'),
            ('in_out','In-Out'),
            ('liquidation','Liquidation'),
            ('low','Low'),
            ('draft', 'Draft'),
            ],'State', index=True, default='draft',
            help="Commercial treatment status\n"
             " * Active: Most of the articles will have this status, it indicates that the product can be bought, sold and distributed freely.\n"
             " * In-Out: Indicates that you should not continue buying. That is bought only once, but it is not continuous.\n"
             " * Liquidation: It tells us that no replacements or purchases should be made. When its stock is finished, the product will be canceled and will not re-enter.\n"
             " * Low: The product will no longer be marketed in the company. Block the sale, purchase and distribution, the stock must be at 0.\n")

    @api.onchange("state")
    def _onchange_state_in_out(self):
        for record in self:
            # if (record.qty_available):
            if record.state == "low" and record.qty_available:
                raise ValidationError("El stock debe estar en 0")

    

    # active = fields.Char(string="Activo")
    # in_out = fields.Char(string="In Out")
    # state_many = fields.Many2one("product.state")

    # state = fields.Many2one(
    #         'activo','Activo',
    #         'in_out','In-Out',
    #         'liquidación','Liquidación',
    #         'baja','Baja',
    #         'draft', 'Draft',
    #         'State', index=True, default='draft',
    #         help="Commercial treatment status\n"
    #          " * Active: Most of the articles will have this status, it indicates that the product can be bought, sold and distributed freely.\n"
    #          " * In-Out: Indicates that you should not continue buying. That is bought only once, but it is not continuous.\n"
    #          " * Settlement: It tells us that no replacements or purchases should be made. When its stock is finished, the product will be canceled and will not re-enter.\n"
    #          " * Low: The product will no longer be marketed in the company. Block the sale, purchase and distribution, the stock must be at 0.\n")

# class ProductState(models.Model):
#     _name = "product.state"
#     _description = "Product State"

#     active = fields.Char(string="Activo")
#     in_out = fields.Char(string="In Out")

    # state_many = fields.Many2one("product.state")
# class SaleOrder(models.Model):

#     _inherit = 'sale.order'
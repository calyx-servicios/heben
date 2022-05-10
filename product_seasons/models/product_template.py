from odoo import models, fields

class ProductTemplate (models.Model):
    _inherit = 'product.template'

    product_seasons_id = fields.Many2one( 'product.seasons',"Temporada", help="Select a season for this product")
    product_material_id = fields.Many2one('product.material', "Material", help="Select a material or this product")
    product_family_id = fields.Many2one('product.family', "family", help="Select a family or this product")
    
    
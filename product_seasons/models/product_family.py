from odoo import api, fields, models

class ProductFamily(models.Model):
    _name = "product.family"
    _description = "Product Familia"
    _order = "name"

    name = fields.Char(compute="_compute_code_name")
    code = fields.Char("Codigo Material", Required=True)
    description = fields.Char("Nombre Familia", Required=True)
    product_ids = fields.One2many(
    "product.template", "product_family_id", string="Familia"
    )

    @api.depends('code','description')
    def _compute_code_name(self):
        for rec in self:
            if rec.code and rec.description:
                rec.name = rec.code + ' ' + rec.description
            elif rec.name and not rec.description:
                rec.name = rec.code
            elif rec.description and not rec.name:
                rec.name = rec.description
            else:
                rec.name = ' '

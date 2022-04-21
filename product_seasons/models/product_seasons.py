from odoo import api, fields, models
from odoo.exceptions import ValidationError

class ProductSeasons(models.Model):
    _name = "product.seasons"
    _description = "Product Seasons"
    _order = "name"

    name = fields.Char(compute="_compute_code_name")
    code = fields.Char("Codigo Material")
    description = fields.Char("Nombre",translate=True,)
    product_ids = fields.One2many(
        "product.template", 
        "product_seasons_id",
        "Temporadas",
    )
    products_count = fields.Integer(
        string="Numero de productos",
        compute="_compute_products_count",
    )

    @api.depends("product_ids")
    def _compute_products_count(self):
        product_model = self.env["product.template"]
        groups = product_model.read_group(
            [("product_seasons_id", "in", self.ids)],
            ["product_seasons_id"],
            ["product_seasons_id"],
            lazy=False,
        )
        data = {group["product_seasons_id"][0]: group["__count"] for group in groups}
        for seasons in self:
            seasons.products_count = data.get(seasons.id, 0)

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

            
    logo = fields.Binary("Logo File")
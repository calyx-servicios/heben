from odoo import api, fields, models

class ProductMaterial(models.Model):
    _name = "product.material"
    _description = "Product Material"
    _order = "name"

    name = fields.Char(compute="_compute_code_name")
    code = fields.Char("Codigo Material")
    description= fields.Char("Nombre", translate=True,)
    product_ids = fields.One2many(
    "product.template", "product_material_id", string="Material"
    )
    products_count = fields.Integer(
        string="Numero de productos", compute="_compute_products_count_material"
    )

    @api.depends("product_ids")
    def _compute_products_count_material(self):
        product_model = self.env["product.template"]
        groups = product_model.read_group(
            [("product_material_id", "in", self.ids)],
            ["product_material_id"],
            ["product_material_id"],
            lazy=False,
        )
        data = {group["product_material_id"][0]: group["__count"] for group in groups}
        for material in self:
            material.products_count = data.get(material.id, 0)

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
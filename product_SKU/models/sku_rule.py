from odoo import models, fields

class SkuRule(models.Model):
    _name = "sku.rule"
    _description = "Sku Rule"
    
    rule_id = fields.Many2one('sku.rule.line')
    mask_sku_id = fields.Many2one('mask.sku')
    sequence = fields.Integer()

class SkuRuleLine(models.Model):
    _name = "sku.rule.line"

    name = fields.Char()
    field_require_rule = fields.Char()
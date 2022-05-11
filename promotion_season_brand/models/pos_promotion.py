# -*- coding: utf-8 -*-
from odoo import fields, models, _

class PosPromotion(models.Model):
    _inherit = 'pos.promotion'

   
    promotion_season_ids = fields.One2many(
        comodel_name="pos.promotion.season",
        inverse_name="promotion_id",
        string=_("Seasons")
    )

    promotion_brand_ids = fields.One2many(
        comodel_name="pos.promotion.brand",
        inverse_name="promotion_id",
        string=_("Brand")
    )


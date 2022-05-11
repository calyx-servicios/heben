# -*- coding: utf-8 -*-
from odoo import fields, models, _

class PosPromotionBrand(models.Model):
    _name = 'pos.promotion.brand'

    promotion_id = fields.Many2one(
        comodel_name="pos.promotion", string=_("Promotion"))
    promotion_code = fields.Char(related='promotion_id.promotion_code',
                                 string=_("Promotion Code"),
                                 store=True)

    state = fields.Selection(
        related='promotion_id.state', string=_('State'), store=True)
    brand_id = fields.Many2one('product.brand', _('Brand'), required=True)
    fixed_price = fields.Float(_('Fixed Price'))
    disc_percentage = fields.Float(_('Disc. %'))
    disc_amount = fields.Float(_('Disc. Amount'))


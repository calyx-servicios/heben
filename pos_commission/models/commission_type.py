from odoo import api, fields, models, _


class CommissionType(models.Model):
    _name = 'commission.type'
    _description = "Commission Type"

    active = fields.Boolean(default=True)
    name = fields.Char(required=True, translate=True)
    sellers_ids = fields.Many2many('hr.employee', string=_("Sellers"))
    sellers = fields.Char(compute="_compute_sellers")
    commission_type = fields.Selection([
        ('standard', 'Standard'),
        ('product_categ', 'Product or Category'),
        ], string='Commission Type', default='standard',
        help=_("Standard - Commission will be provided as percentage or fixed amount.\n") +
            _("Product or Category - Commission will be provided as percentage or fixed amount.\n"))
    standard_commission_type = fields.Selection([
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
        ], string=_('Standard Commission'),
        help=_("Percentage - Commission will be provided as percentage.\n") +
            _("Fixed - Commission will be provided as fixed amount \n"))
    # Standard percentage
    percentage_commission = fields.Integer()
    # Standard fixed
    fixed_commission = fields.Integer()
    # Product or Category
    commission_apply = fields.Selection([
        ('all_products', 'All Products'),
        ('category', 'Product Category'),
        ('product', 'Product'),
        ], string=_('Standard Commission'), default='all_products',
        help=_("All Products - Commission will be provided in all the products\n") +
            _("Product Category - Commission will be provided in the selected categories \n") +
            _("Product - Commission will be provided in the selected products \n"))
    commission_line_ids = fields.One2many('commission.type.line','commission_type_id')
    commission_price = fields.Char(compute="_compute_commission_price")
    commission_line_products = fields.Char(compute="_compute_commission_line_product")

    @api.depends('commission_line_ids','commission_type')
    def _compute_commission_line_product(self):
        for rec in self:
            object_list = []
            for commission in rec.commission_line_ids:
                if commission.applied_on == '3_global':
                    object_list.append(_('All Products'))
                if commission.applied_on == '2_product_category':
                    for category in commission.categ_id:
                        object_list.append(category.name)
                if commission.applied_on == '1_product':
                    for category in commission.product_tmpl_id:
                        object_list.append(category.name)
                if commission.applied_on == '0_product_variant':
                    for category in commission.product_id:
                        object_list.append(category.name)
            
            if len(object_list) == 1:
                rec.commission_line_products = object_list[0]
            elif rec.commission_type == 'standard':
                rec.commission_line_products = _('All Products')
            else:    
                rec.commission_line_products = _("Multiple")

    @api.depends('sellers_ids')
    def _compute_sellers(self):
        for rec in self:
            if len(rec.sellers_ids.ids) == 1:
                rec.sellers = rec.sellers_ids[0].name
            else:
                rec.sellers = _("Multiple")

    @api.onchange('commission_type')
    def _onchange_commission_type(self):
        for rec in self:
            if rec.commission_type == 'product_categ':
                rec.standard_commission_type = False
            if rec.commission_type == 'standard':
                rec.commission_line_ids = False

    @api.depends('percentage_commission','fixed_commission')
    def _compute_commission_price(self):
        computed_price = ''
        for rec in self:
            if rec.standard_commission_type == 'fixed':
                computed_price = '$ ' + str(rec.fixed_commission) 
            if rec.standard_commission_type == 'percentage':
                computed_price = str(rec.percentage_commission) + ' %'
            if rec.commission_type == 'product_categ':
                if len(rec.commission_line_ids.ids) == 1:
                    computed_price = rec.commission_line_ids[0].computed_price
                else:
                    computed_price = _("Multiple")
            rec.commission_price = computed_price

class CommissionTypeLine(models.Model):
    _name = "commission.type.line"
    _description = "Commission Line"

    commission_type_id = fields.Many2one(
        'commission.type', ondelete='cascade')
    product_tmpl_id = fields.Many2many(
        'product.template', string=_('Product'),
        help=_("Specify a template if this rule only applies to one product template. Keep empty otherwise."))
    product_id = fields.Many2many(
        'product.product', string=_('Product Variant'),
        help=_("Specify a product if this rule only applies to one product. Keep empty otherwise."))
    categ_id = fields.Many2many(
        'product.category', string=_('Product Category'),
        help=_("Specify a product category if this rule only applies to products belonging to this category or its children categories. Keep empty otherwise."))
    applied_on = fields.Selection([
        ('3_global', 'All Products'),
        ('2_product_category', 'Product Category'),
        ('1_product', 'Product'),
        ('0_product_variant', 'Product Variant')], _("Apply On"),
        default='3_global', required=True,
        help=_('Pricelist Item applicable on selected option'))
    compute_price = fields.Selection([
        ('fixed', 'Fixed Price'),
        ('percentage', 'Percentage (discount)')], index=True, default='fixed', required=True)
    fixed_price = fields.Float(_('Fixed Price'), digits='Product Price')
    percent_price = fields.Float(_('Percentage Price'))
    apply_on = fields.Char(compute="_compute_apply_on")
    computed_price = fields.Char(compute="_compute_computed_price")

    @api.depends('categ_id','product_tmpl_id','product_id')
    def _compute_apply_on(self):
        object_list = []
        for rec in self:
            object_list = []
            if rec.applied_on == '3_global':
                object_list.append(_('All Products'))
            if rec.applied_on == '2_product_category':
                for category in rec.categ_id:
                    object_list.append(category.name)
            if rec.applied_on == '1_product':
                for category in rec.product_tmpl_id:
                    object_list.append(category.name)
            if rec.applied_on == '0_product_variant':
                for category in rec.product_id:
                    object_list.append(category.name)
            rec.apply_on = str(' - '.join(object_list))

    @api.depends('fixed_price','percent_price')
    def _compute_computed_price(self):
        computed_price = ''
        for rec in self:
            if rec.compute_price == 'fixed':
                computed_price = '$ ' + str(rec.fixed_price) 
            if rec.compute_price == 'percentage':
                computed_price = str(rec.percent_price) + ' %'
            rec.computed_price = computed_price


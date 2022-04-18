# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_compare
from odoo.tools.misc import formatLang
from dateutil.relativedelta import relativedelta


# class AccountMove(models.Model):
#     _inherit = 'account.move'

    # partner_id_variants = fields.Integer(string="Id", related="partner_id.id" )
    # prueba = fields.Integer(string="prueba", related="partner_id.id")
    # product_id = fields.Many2one('product.product', string='Productkkg', ondelete='restrict', domain=[('state', '=', 'in_out')])
# states={'in_out': [('invisible', True)]}

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    product_id = fields.Many2one('product.product')
    # prueba_dos = fields.Char(string="prueba")


# coding: utf-8
# import logging

# from odoo import models, fields, api, _
# from odoo.exceptions import MissingError


# class AccountMove(models.Model):
#     _inherit = "account.move"
# class AccountMoveLine(models.Model):
#     _name = "account.move.line"
#     _description = "Journal Item"
#     _order = "date desc, move_name desc, id"
#     _check_company_auto = True

# product_id = fields.Many2one('product.product', string='Productkkg', ondelete='restrict', domain="[('state', '=', 'draft')]")
# states={'in_out': [('invisible', True)]}


#  domain=[("context.get('default_type') in ('out_invoice', 'out_refund', 'out_receipt') and [('sale_ok', '=', True), '|', ('company_id', '=', False), ('company_id', '=', parent.company_id)] or [('purchase_ok', '=', True), '|', ('company_id', '=', False), ('company_id', '=', parent.company_id), ('state', '=', 'in_out')]")]
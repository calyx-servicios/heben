from odoo import fields, models, api, _
from odoo.exceptions import UserError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    country_key = fields.Char('Country key')
    company_key = fields.Char('Company key')


    @api.model
    def get_values(self):
        # Object
        ir_config_parameter_obj = self.env['ir.config_parameter'].sudo()

        # Get current settings values
        values = super(ResConfigSettings, self).get_values()

        values.update(
            country_key=ir_config_parameter_obj.get_param('country.key'),
            company_key=ir_config_parameter_obj.get_param('company.key'),
        )

        return values

    def set_values(self):
        # Objects
        ir_config_parameter_obj = self.env['ir.config_parameter'].sudo()

        # Set values
        super(ResConfigSettings, self).set_values()

        # Save module values
        ir_config_parameter_obj.set_param('country.key', self.country_key)
        ir_config_parameter_obj.set_param('company.key', self.company_key)

    @api.model
    def product_barcode_get_settings(self):
        # Get settings values
        values = self.get_values()

        # Validate country_key and company_key here
        country_key = values.get('country_key')
        company_key = values.get('company_key')

        if not country_key or not country_key.isdigit() or len(country_key) != 3:
            raise UserError(_('Invalid country key on settings. It must be a 3-digit number.'))

        if not company_key or not company_key.isdigit() or len(company_key) != 4:
            raise UserError(_('Invalid company key on settings. It must be a 4-digit number.'))

        # Parse dict values.
        return dict([
            ('COUNTRY_KEY', country_key),
            ('COMPANY_KEY', company_key),
        ])

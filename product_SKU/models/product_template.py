from odoo.exceptions import UserError, ValidationError
from odoo import models, fields, api

class ProductProduct (models.Model):
    _inherit = 'product.product'

    product_sku_id = fields.Many2one('product.sku',string="Internal Reference", help="Select a rule sku for this product")
    use_sku = fields.Boolean('Use Sku')
     
    # when product_sku_id field detect change going to shoot def onchage_product_sku_id
    @api.onchange('product_sku_id')
    def onchage_product_sku_id(self):
        if self.product_sku_id:
            # dictionary type variable that stores the codes of the fields required in the rule
            fields_model = {
                'product_family_id': self.product_family_id.code,
                'product_material_id': self.product_material_id.code,
                'product_season_id': self.product_seasons_id.code,
                'internal_code': self.internal_code
            }
            # variable that filters the color or size attribute in the product_template_attribute_value_ids field
            variant_color_id = self.product_template_attribute_value_ids.filtered(lambda attribute: attribute.display_type == 'color')[0].product_attribute_value_id
            variant_talle_id = self.product_template_attribute_value_ids.filtered(lambda attribute: attribute.display_type == 'talle')[0].product_attribute_value_id
            # variable in which the rule is mapped in each object that would be code_list in each product_sku_id
            code_list_model = self.product_sku_id.code_list.mapped('rule')
            # variable indicating that the field is complete
            fields_required_success = True
            # variable that stores error message 
            fields_required_error = ''
            # variable that stores the result of the rule
            default_code_sku = ''
            # for 
            for code_field in code_list_model:
                # si code_field de la regla es talle y no tiene una variante definida la variable fields_required_success es falsa y por lo tanto tira error 'Falta definir talle' > en ese caso sale del for por el error
                if  code_field.is_talle and not variant_talle_id:
                    fields_required_success = False
                    fields_required_error = 'Falta definir Talle'
                    break
                # pero si code_field es talle y tiene la variante definida, almacena en default_Code_sku el codigo de la variante >  continua el for
                elif code_field.is_talle and variant_talle_id:
                    default_code_sku += variant_talle_id.code
                    continue
                # si code_field de la regla es color y no tiene una variante definida la variable fields_required_success es falsa y por lo tanto tira error 'Falta definir  olor' > en ese caso sale del for por el error
                if  code_field.is_color and not variant_color_id:
                    fields_required_success = False
                    fields_required_error = 'Falta definir Color'
                    break
                # pero si code_field es color y tiene la variante definida, almacena en default_Code_sku el codigo de la variante >  continua el for
                elif code_field.is_color and variant_color_id:
                    default_code_sku += variant_color_id.code
                    continue
                #  en cada regla el campo field_require_rule
                if code_field.field_require_rule:
                    # si no esta definido el campo tira error Falta definir el campo requerido en la regla > por lo tanto sale del for
                    if not fields_model[code_field.field_require_rule]:
                        fields_required_success = False
                        fields_required_error = ('Falta definir el campo %s') % (code_field.name)
                        break
                    # si esta definido lo almacena en el campo default_code_sku > continua el for
                    else:
                        default_code_sku += fields_model[code_field.field_require_rule]
                        continue
            # si no esta definido fields_required_success tira un ValidationError con los campos no definidos
            if not fields_required_success:
                raise ValidationError(fields_required_error)
            # si esta todo definido almaceno en  default_code lo guardado en default_code_sku
            else:
                self.default_code = default_code_sku
            
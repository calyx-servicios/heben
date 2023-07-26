{
    "name": "Argentina - Product Barcode",
    "summary": """
    This module generates, according to Argentine regulations, the barcode for the product.
    """,
    "author": "Calyx Servicios S.A.",
    "maintainers": ["Zamora, Javier"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Custom",
    "version": "13.0.1.0.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "depends": [
        'base',
        'product_barcode',
    ],
    "data": [
        'views/res_config_settings.xml',
        'data/ir_config_parameter.xml',
    ],
}

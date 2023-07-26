{
    "name": "Magento Product Export",
    "summary": """
        This module generates a customized Excel file for easily exporting products to Magento.
    """,
    "author": "Calyx Servicios S.A.",
    "maintainers": ["Zamora, Javier"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Custom",
    "version": "13.0.1.1.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "depends": ['globalteckz_magento_2', 'report_xlsx'],
    "data": [
        'views/action_menu.xml',
        'report/magento_product_export.xml',
    ],
}

# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Cron Import orders magento",
    "summary": """
        """,
    "author": "Calyx Servicios S.A.",
    "maintainers": ["ParadisoCristian"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Custom",
    "version": "13.0.2.0.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "depends": ['globalteckz_magento_2'],
    "data": [
        'data/ir_cron.xml',
    ],
}

# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Automation Ecommerce Sales",
    "summary": """
        This module adds the automation of the Ecommerce Sales process
    """,
    "author": "Calyx Servicios S.A.",
    "maintainers": ["PerezGabriela"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Sale",
    "version": "13.0.1.2.2",
    "installable": True,
    "application": False,
    "depends": [
        'globalteckz_magento_2',
        'location_by_proximity',
        'pos_sale_chat',
        'melisync'
    ],
    "data": [
        'data/data.xml',
        'data/ir_cron.xml'
    ],
}

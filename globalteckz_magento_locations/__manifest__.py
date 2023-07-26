# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Globalteckz Magento Locations",
    "summary": """
        This module updates cron and locations
    """,
    "author": "Calyx Servicios S.A.",
    "maintainers": ["ParadisoCristian"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Connector",
    "version": "13.0.1.0.0",
    "installable": True,
    "application": False,
    "depends": [
        'globalteckz_magento_2',
    ],
    "data": [
        'views/gt_magento_shop_view.xml',  
    ],
}

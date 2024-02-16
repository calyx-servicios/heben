# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "POS sale chat",
    "summary": """
        This module adds the stock reservation notice to the pos
    """,
    "author": "Calyx Servicios S.A.",
    "maintainers": ["PerezGabriela","EnzoGonzalezDev"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Sale",
    "version": "13.0.4.0.2",
    "installable": True,
    "application": False,
    "depends": [
        'sale',
        'stock',
        'point_of_sale_chat'
    ],
    "data": [
        'data/ir_actions.xml',
        'data/ir_cron.xml',
    ],
}

# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Invoice Untaxed",
    "summary": """
        This module adds the functionality of invoicing without taxes
    """,
    "author": "Calyx Servicios S.A.",
    "maintainers": ["PerezGabriela"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Invoice",
    "version": "13.0.1.0.0",
    "application": False,
    "installable": True,
    "depends": [
        'purchase',
        'sale'
    ],
    "data": [
    ],
}

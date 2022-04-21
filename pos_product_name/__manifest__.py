# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Point of sale product name",
    "summary": """
            This module changes the name of the product
            at the point of sale
        """,
    "author": "Calyx Servicios S.A.",
    "maintainers": ["PerezGabriela"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Custom",
    "version": "13.0.1.1.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "external_dependencies": {"python": [], "bin": []},
    "depends": ['point_of_sale'],
    "data": [
        "views/point_of_sale.xml",
    ],
}

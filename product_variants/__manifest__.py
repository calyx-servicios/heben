# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Activity brands",
    "summary": """
            This module provides information on the activity marks of the products
        """,
    "author": "Calyx Servicios S.A.",
    "maintainers": [""],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Product",
    "version": "13.0.1.0.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "external_dependencies": {"python": [], "bin": []},
    "depends": ['product', 'base'],
    "data": [
        'views/product_variants_view.xml',
        
    ],
}

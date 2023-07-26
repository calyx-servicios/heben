# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product Rotation",
    "summary": """
            This module provides information on the activity marks of the products
        """,
    "author": "Calyx Servicios S.A.",
    "maintainers": ["marcooegg"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Product",
    "version": "13.0.0.0.1",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "external_dependencies": {"python": [], "bin": []},
    "depends": ['base','product', 'sale_stock','account', 'stock','sale'],
    "data": [
        "security/ir.model.access.csv",
        "views/product_color_search_views.xml",
        "report/product_report_views.xml",
    ],
}

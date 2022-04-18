# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product Seasons",
    "summary": "Product Seasons",
    "author": "Calyx Servicios S.A.",
    "maintainers": ["Georgina Guzman"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "category": "Custom",
    "version": "13.0.1.0.0",
    "application": False,
    "license": "AGPL-3",
    "external_dependencies": {"python": [], "bin": []},
    "depends": ["sale","stock","stock_account"],
    "data": [
        "views/product_season_view.xml",
        "views/product_template_view.xml",
        "views/product_material_view.xml",
        "views/product_family_view.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
    "auto_install": False,
}

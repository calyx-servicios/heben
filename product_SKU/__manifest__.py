# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product SKU",
    "summary": "Generate Product SKU",
    "author": "Calyx Servicios S.A.",
    "maintainers": ["marcooegg", "garaceliguzman"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "category": "Custom",
    "version": "13.0.1.0.0",
    "application": False,
    "license": "AGPL-3",
    "external_dependencies": {"python": [], "bin": []},
    "depends": ["sale","stock","stock_account","product_seasons"],
    "data": [
        "views/product_sku_view.xml",
        "views/product_attribute_value.xml",
        "security/ir.model.access.csv",
        "data/data.xml",
    ],
    "installable": True,
    "auto_install": False,
}

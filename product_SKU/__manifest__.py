# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product SKU",
    "summary": "Generate Product SKU",
    "author": "Calyx Servicios S.A.",
    "maintainers": ["marcooegg", "garaceliguzman","ParadisoCristian", "PerezGabriela"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "category": "Custom",
    "version": "13.0.3.0.1",
    "application": False,
    "license": "AGPL-3",
    "depends": ["sale","stock","stock_account","product_seasons", "default_code_products"],
    "data": [
        "security/ir.model.access.csv",
        "data/data.xml",
        "views/product_attribute_value_view.xml",
        "views/product_product_view.xml",
        "views/product_template_view.xml",
        "views/product_sku_view.xml",
        "wizard/massive_sku_wizard_views.xml"
    ],
    "installable": True,
    "auto_install": False,
}

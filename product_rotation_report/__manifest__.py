# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product Rotation Report",
    "summary": """
            This module provides information on the activity marks of the products
        """,
    "author": "Calyx Servicios S.A.",
    "maintainers": ["gpperez"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Product",
    "version": "13.0.0.0.1",
    "development_status": "Production/Stable",
    "depends": ['base', 'product', 'sale_stock', 'account', 'stock'],
    "data": [
        "security/ir.model.access.csv",
        "report/product_rotation_report_views.xml",
    ],
    "pre_init_hook": "pre_init_hook",
    "uninstall_hook": "uninstall_hook",
    "application": False,
    "installable": True,

}

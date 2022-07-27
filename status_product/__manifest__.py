# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product status",
    "summary": """
        This module adds states to products.
    """,
    "author": "Calyx Servicios S.A.",
    "maintainers": ["AndresAndrade", "PerezGabriela"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Custom",
    "version": "13.0.2.0.0",
    "installable": True,
    "application": False,
    "depends": [
        'product',
        'base',
        'account_reports',
        'sale'
    ],
    "data": [
        'views/product_status_view.xml',
        'views/account_move_view.xml',
        'views/sale_order_view.xml',
        'views/purchase_order_view.xml',  
    ],
}

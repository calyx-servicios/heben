# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product status",
    "summary": """
            this module is to be able to provide more information to the products
        """,
    "author": "Calyx Servicios S.A.",
    "maintainers": [""],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Custom",
    "version": "11.0.1.0.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "external_dependencies": {"python": [], "bin": []},
    "depends": ['product', 'base','account_reports'],
    "data": [
        'views/product_status_view.xml',
        'views/account_move_view.xml',
        'views/sale_order_view.xml',
        'views/purchase_order_view.xml',
        
    ],
}

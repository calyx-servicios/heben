# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Stock Reserve",
    "summary": """
        """,
    "author": "Calyx Servicios S.A.",
    "maintainers": ["AndresAndrade"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Custom",
    "version": "13.0.1.0.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "external_dependencies": {"python": [], "bin": []},
    # "depends": ['product', 'base','account_reports'],
    "depends": ['product', 'base', 'stock', 'sale'],
    "data": [
        'views/stock_location_view.xml',
        'views/sale_order_line_view.xml',
    ],
}

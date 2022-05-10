# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Contact Field",
    "summary": """
            This module adds a contact field in inventory
        """,
    "author": "Calyx Servicios S.A.",
    "maintainers": [""],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Custom",
    "version": "13.0.1.0.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "external_dependencies": {"python": [], "bin": []},
    # "depends": ['product', 'base','account_reports'],
    "depends": ['product', 'base', 'stock'],
    "data": [
        'views/stock_warehouse_view.xml',
    ],
}

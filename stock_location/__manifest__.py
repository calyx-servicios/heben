{
    "name": "Stock Location",
    "summary": """ This module adds fields in nearby stock reservation 
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
    "depends": ['product', 'base', 'stock','sale'],
    "data": [
        'views/stock_location_view.xml',
        'views/sale_order_line_view.xml',
    ],
}
{
    "name": "Location by Proximity",
    "summary": """ This module adds fields in nearby stock reservation 
        """,
    "author": "Calyx Servicios S.A.",
    "maintainers": ["ParadisoCristian"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Custom",
    "version": "13.0.2.0.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "depends": ['stock','sale'],
    "data": [
        'views/stock_location_view.xml',
        'views/sale_order_line_view.xml',
        'data/mail_data.xml',
    ],
}

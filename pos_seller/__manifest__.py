# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Point of sale seller",
    "summary": """
            This module adds a seller to the point of sale
        """,
    "author": "Calyx Servicios S.A.",
    "maintainers": ["PerezGabriela"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Custom",
    "version": "13.0.4.2.2",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "external_dependencies": {"python": [], "bin": []},
    "depends": ['point_of_sale'],
    "data": [
        "views/point_of_sale.xml",
        "views/pos_config.xml",
        "views/pos_order_view.xml",
        "views/pos_order_report_view.xml",
    ],
    'qweb': [
        'static/src/xml/pos.xml',
    ],
}

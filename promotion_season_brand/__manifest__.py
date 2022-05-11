# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Promotion season brand",
    "summary": """
        This module adds the filter by season and 
        brand to the promotions.
    """,
    "author": "Calyx Servicios S.A.",
    "maintainers": ["PerezGabriela"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Point of sale",
    "version": "13.0.1.0.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "external_dependencies": {"python": [], "bin": []},
    "depends": [
        "point_of_sale",
        "product_seasons", 
        "pos_promotion_niq", 
        "product_brand_inventory"
    ],
    "data": [
        'security/ir.model.access.csv',
        'views/pos_promotion_views.xml',
        'views/point_of_sale_assets.xml',
    ],
}

# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product Curve",
    "summary": """
        This module adds the curve for products
    """,
    "author": "Calyx Servicios S.A.",
    "maintainers": ["PerezGabriela","DeykerGil"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Sale",
    "version": "13.0.3.4.1",
    "installable": True,
    "application": False,
    "depends": [
        'base', 
        'sale', 
        'stock',
        'product', 
        'product_matrix', 
        'sale_management', 
        'purchase', 
        'purchase_requisition',
        'status_product',
        'stock_picking_batch_extended_custom'
    ],
    "data": [
        'views/assets.xml',
        'views/product_curve.xml',
    ],
}

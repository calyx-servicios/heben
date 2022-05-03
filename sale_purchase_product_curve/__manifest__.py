# -*- coding: utf-8 -*-
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
    "version": "13.0.1.0.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "external_dependencies": {"python": [], "bin": []},
    "depends": [
        'base', 
        'sale', 
        'product', 
        'product_matrix', 
        'sale_management', 
        'purchase', 
        'purchase_requisition'
    ],
    "data": [
        'views/assets.xml',
        'views/product_curve.xml',
    ],
}

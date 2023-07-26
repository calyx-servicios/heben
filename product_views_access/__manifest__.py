# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Product Views Access',
    'summary': """
        This module adds the permissions for product views.
    """,
    'author': 'Calyx Servicios S.A.',
    'maintainers': ['PerezGabriela'],
    'website': 'http://odoo.calyx-cloud.com.ar/',
    'license': 'AGPL-3',
    'category': 'Stock',
    'version': '13.0.2.0.0',
    'application': False,
    'installable': True,
    'depends': [
        'point_of_sale',
        'website_sale'
    ],
    'data': [
        'security/product_views_access_security.xml',
        'views/product_views.xml',
    ],
}

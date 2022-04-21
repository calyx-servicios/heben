# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Point of sale commission",
    "summary": """
        This module adds the commissions for sellers
    """,
    "author": "Calyx Servicios S.A.",
    "maintainers": ["ParadisoCristian"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Point of sale",
    "version": "13.0.1.0.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "external_dependencies": {"python": [], "bin": []},
    "depends": ['pos_seller','account'],
    "data": [
        'security/ir.model.access.csv',
        'wizard/pos_commission_wizard_views.xml',
        'views/commission_type_views.xml',
        'views/commission_view.xml',
        'views/account_journal_views.xml',
    ],
}

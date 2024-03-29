# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Point of sale commission",
    "summary": """
        This module adds the commissions for sellers
    """,
    "author": "Calyx Servicios S.A.",
    "maintainers": ["ParadisoCristian", "PerezGabriela"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Point of sale",
    "version": "13.0.3.0.4",
    "application": False,
    "installable": True,
    "depends": [
        'pos_seller',
        'account'
    ],
    "data": [
        'security/ir.model.access.csv',
        'wizard/pos_commission_wizard_views.xml',
        'views/commission_type_views.xml',
        'views/commission_view.xml',
        'views/account_journal_views.xml',
    ],
}

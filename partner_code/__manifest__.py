# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Partner Code",
    "summary": """
            this module adds the partner code field
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
    "depends": ['product'],
    "data": [
        'views/partner_code_view.xml',
        
    ],
}

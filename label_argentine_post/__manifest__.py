# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "labeled Argentine mail",
    "summary": """
        create label for Argentine mail""",
    "author": "Calyx Servicios S.A.",
    "maintainers": ["GeorginaGuzman"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Stock",
    "version": "13.0.1.0.0",
    "development_status": "Production/Stable",
    "depends": ['base','stock'],
    "data": [
        'security/ir.model.access.csv',
        "views/template_in_address.xml",
        "views/template_in_branch.xml",
        "views/argentine_post_branch.xml",
        "views/stock_picking_view.xml",
    ],
}

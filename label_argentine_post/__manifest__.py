# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Labeled Argentine post",
    "summary": """
        Create label for Argentine post""",
    "author": "Calyx Servicios S.A.",
    "maintainers": ["GeorginaGuzman","PerezGabriela"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Stock",
    "version": "13.0.2.0.2",
    "development_status": "Production/Stable",
    "installable": True,
    "application": False,
    "depends": ['base','stock'],
    "data": [
        'security/ir.model.access.csv',
        "views/template_in_address.xml",
        "views/template_in_branch.xml",
        "views/argentine_post_branch.xml",
        "views/stock_picking_view.xml",
    ],
}

# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Stock batch picking Custom",
    "summary": """
        Add modifications to the module stock picking batch extended
    """,
    "author": "Calyx Servicios S.A.",
    "maintainers": ["DarwinAndrade","ParadisoCristian","PerezGabriela"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Custom",
    "version": "13.0.2.3.1",
    "installable": True,
    "application": False,
    "depends": ["stock_picking_batch_extended"],
    "data": [
        "wizard/missing_picking_wizard_view.xml",
        "security/ir.model.access.csv",
        "views/stock_batch_picking.xml",
    ],
}

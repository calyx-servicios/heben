{
    "name": "Stock batch picking Custom",
    "summary": "Add modifications to the module stock picking batch extended",
    "version": "13.0.1.3.0",
    "author": "Calyx Servicios S.A.",
    "development_status": "Production/Stable",
    "maintainers": ["DarwinAndrade","ParadisoCristian"],
    "category": "Custom",
    "depends": ["stock_picking_batch", "delivery", "stock_picking_batch_extended"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "data": [
        "security/ir.model.access.csv",
        "views/stock_batch_picking.xml",
    ],
    "installable": True,
    "license": "AGPL-3",
}

# Copyright 2012-2014 Alexandre Fayolle, Camptocamp SA
# Copyright 2018-2020 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Stock batch picking Custom",
    "summary": "Add modifications to the module stock picking batch extended",
    "version": "13.0.1.3.0",
    "author": "Calyx Servicios S.A.",
    "development_status": "Production/Stable",
    "maintainers": ["DarwinAndrade"],
    "category": "Custom",
    "depends": ["stock_picking_batch", "delivery", "stock_picking_batch_extended"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "data": [
        "views/stock_batch_picking.xml",
    ],
    "installable": True,
    "license": "AGPL-3",
}

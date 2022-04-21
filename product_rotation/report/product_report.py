from odoo import models, fields, api, _
from odoo import tools
import logging

_logger = logging.getLogger(__name__)


class ProductReport(models.Model):
    _name = "product.report"
    _description = "Product Report"
    _auto = False
    _rec_name = "product_name_and_color"
    _order = "date desc"

    # queried fields:
    date = fields.Date(string="Move Date")
    product_id = fields.Many2one(
        comodel_name="product.product", string="Product", readonly=True
    )
    product_name_and_color = fields.Char(string="Product Name and Color", readonly=True)
    location_id = fields.Many2one(
        comodel_name="stock.location", string="Stock Location", readonly=True
    )
    # qty_available = fields.Float(string="Available Quantity", readonly=True)
    company_id = fields.Many2one(comodel_name='res.company', string='Company', readonly=True)
    qty_sold = fields.Float(string='Quantity Sold', readonly=True)
    categ_id = fields.Many2one(comodel_name='product.category', string='Category', readonly=True)
    brand_id = fields.Many2one(comodel_name='product.brand', string='Brand', readonly=True)
    product_seasons_id = fields.Many2one(comodel_name='product.seasons', string='Season', readonly=True)
    product_family_id = fields.Many2one(comodel_name='product.family', string='Family', readonly=True)
    product_material_id = fields.Many2one(comodel_name='product.material', string='Material', readonly=True)
    qty_received = fields.Float(string='Quantity Received', readonly=True)
    move_line_id = fields.Many2one(comodel_name='stock.move.line', string='Move', readonly=True)
    balance = fields.Float(string='balance', readonly=True)

    


    def _query(self, with_clause="", fields={}, groupby="", from_clause="", where=""):
        with_clause = """
            customer_location as (SELECT id FROM stock_location WHERE usage = 'customer' LIMIT 1)
        """

        with_ = ("WITH %s" % with_clause) if with_clause else ""

            # max(sq.quantity) as qty_available,
        select_ = """
            min(pp.id) as id,
            pp.id as product_id,
            pt.categ_id as categ_id,
            pt.brand_id as brand_id,
            pt.product_seasons_id as product_seasons_id,
            pt.product_family_id as product_family_id,
            pt.product_material_id as product_material_id,
            pp.product_name_and_color as product_name_and_color,
            CASE WHEN sl.usage = 'internal'
                THEN sml.location_dest_id
                WHEN sl.id = cl.id
                THEN sml.location_id
                ELSE 0
                END as location_id,
            sml.company_id as company_id,
            CASE WHEN sl.usage = 'internal'
                THEN qty_done
                ELSE 0
                END as qty_received,
            CASE WHEN sl.id = cl.id
                THEN qty_done
                ELSE 0
                END as qty_sold,
            (SELECT SUM(CASE
                            WHEN sl2.usage = 'internal'
                            THEN sml2.qty_done
                            WHEN sl2.id = cl.id
                            THEN (-sml2.qty_done)
                            ELSE 0
                        END
                        ) as balance
                FROM product_product  pp2
                JOIN stock_move_line sml2 ON pp2.id = sml2.product_id
                JOIN stock_location sl2 ON sl2.id = sml2.location_dest_id
                JOIN customer_location cl2 ON 1 = 1
                WHERE pp2.id = pp.id 
                    AND sml2.date <= sml.date
                LIMIT 1) as balance,
            sml.date as date,
            sml.id as move_line_id
        """
        other = """
            with customer_location as (select id from stock_location where usage = 'customer')
            select date,pp.product_name_and_color,sl.name as desde, sdl.name as hasta, qty_done,
            COALESCE(
                SUM(CASE
                    WHEN sml.location_dest_id = sdl.id
                    THEN sml.qty_done
                    WHEN sml.location_id = sdl.id
                    THEN -sml.qty_done
                    ELSE 0
                    END)
                ,0) as qty_received
            from stock_move_line sml
                inner join product_product pp on pp.id = product_id
                inner join stock_location sl on sl.id = sml.location_id
                inner join stock_location sdl on sdl.id = sml.location_dest_id
                left join customer_location on customer_location.id = sdl.id
            where product_id = 619
            group by date,pp.product_name_and_color,sl.name, sdl.name, qty_done;
        """


        for field in fields.values():
            select_ += field

        

        from_ = """
            product_product as pp
            LEFT JOIN product_template pt on pp.product_tmpl_id = pt.id
            JOIN stock_move_line sml ON sml.product_id = pp.id
                AND sml.state = 'done'
            LEFT JOIN stock_location sl on sl.id = sml.location_dest_id
            LEFT JOIN customer_location cl on 1 = 1

        """

        where_ = f"""
            pp.product_color IS NOT NULL
            {where}
        """

        groupby_ = f"""
            pp.id,
            pt.categ_id,
            pt.brand_id,
            pt.product_seasons_id,
            pt.product_family_id,
            pt.product_material_id,
            pp.product_name_and_color,
            sml.location_id,
            sml.company_id,
            sml.date,
            sml.id,
            sl.usage,
            cl.id,
            sl.id,
            sml.location_dest_id,
            sml.qty_done
            {where}
        """

        _logger.info("%s (SELECT %s FROM %s WHERE %s GROUP BY %s)" % (
            with_,
            select_,
            from_,
            where_,
            groupby_,
        ))
        return "%s (SELECT %s FROM %s WHERE %s GROUP BY %s)" % (
            with_,
            select_,
            from_,
            where_,
            groupby_,
        )

    def init(self):
        # self._table = sale_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            """CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query())
        )


# class SaleOrderReportProforma(models.AbstractModel):
#     _name = 'report.sale.report_saleproforma'
#     _description = 'Proforma Report'

#     def _get_report_values(self, docids, data=None):
#         docs = self.env['sale.order'].browse(docids)
#         return {
#             'doc_ids': docs.ids,
#             'doc_model': 'sale.order',
#             'docs': docs,
#             'proforma': True
# }

        # select_ = """
        #     min(pp.id) as id,
        #     pp.id as product_id,
        #     pt.categ_id as categ_id,
        #     pt.brand_id as brand_id,
        #     pt.product_seasons_id as product_seasons_id,
        #     pt.product_family_id as product_family_id,
        #     pt.product_material_id as product_material_id,
        #     pp.product_name_and_color as product_name_and_color,
        #     sml.location_id as location_id,
        #     sl.company_id as company_id,
        #     COALESCE(
        #         SUM(CASE
        #             WHEN sml.location_dest_id = customer_location.id AND sml.location_id = sl.id
        #             THEN sml.qty_done
        #             ELSE 0
        #             END)
        #         ,0) as qty_sold,
        #     COALESCE(
        #         SUM(CASE
        #             WHEN sml.location_dest_id = sdl.id
        #             THEN sml.qty_done
        #             WHEN sml.location_id = sdl.id
        #             THEN -sml.qty_done
        #             ELSE 0
        #             END)
        #         ,0) as qty_received,
        #     sml.date as date,
        #     sml.id as move_line_id
        # """
        # AND sl.name NOT LIKE '/customer%'
        # from_ = f"""
        #     product_product as pp
        #     LEFT JOIN product_template pt on pp.product_tmpl_id = pt.id
        #     LEFT JOIN stock_move_line sml ON sml.product_id = pp.id
        #         AND sml.qty_done > 0
        #     LEFT JOIN stock_location sl ON sl.id = sml.location_id
        #     LEFT JOIN stock_location sdl ON sdl.id = sml.location_dest_id
        #     LEFT JOIN customer_location on customer_location.id = sdl.id
        #     {from_clause}
        # """
        # _logger.info(f"from_: {from_}")
        #TODO: 
        # LEFT JOIN stock_quant sq ON sq.product_id = pp.id
        # sq.location_id as location_id,
        # change sdl.id = sq.location_id,
        # group by sq.location_id,
        # _logger.info(f"")
        # AND (sl.company_id IS NOT NULL
        #     OR sl.company_id = {self.env.user.company_id.id})
        # AND (sl.usage = 'internal'
        #     OR sl.usage = 'inventory')
        # LEFT JOIN stock_move_line sml ON sml.product_id = pp.id
        # LEFT JOIN sale_order_line sol ON sol.product_id = pp.id
            # AND (
            #     sl.usage = 'internal'
            #     OR
            #     sdl.usage = 'internal'
            # )
        # incoming_moves as (
        #     SELECT
        #         pp.id as product_id,
        #         pp.product_name_and_color as product,
        #         sl.id as location_dest_id,
        #         sl.name as name,
        #         sum(sml.qty_done) as qty_received
        #     FROM
        #         stock_move_line as sml
        #     INNER JOIN product_product pp on pp.id = sml.product_id
        #     INNER JOIN stock_location sl on sl.id = sml.location_dest_id
        #     WHERE sl.usage = 'internal'
        #     GROUP BY sl.id,pp.product_name_and_color, sl.name, pp.id
        #     ORDER BY pp.product_name_and_color, sl.name
        # ),
        # outgoing_moves as (
        #     SELECT
        #         pp.id as product_id,
        #         pp.product_name_and_color as product,
        #         sl.id as location_id,
        #         sl.name as name,
        #         SUM(CASE
        #             WHEN sml.location_dest_id = cl.id AND sml.location_id = sl.id
        #             THEN sml.qty_done
        #             ELSE 0
        #             END) as qty_sold
        #     FROM stock_move_line as sml
        #     INNER JOIN product_product pp on pp.id = sml.product_id
        #     INNER JOIN stock_location sl on sl.id = sml.location_id
        #     INNER JOIN (SELECT id FROM stock_location WHERE usage = 'customer' LIMIT 1) cl on sml.location_dest_id = cl.id
        #     WHERE pp.id between 610 and 632
        #     GROUP BY sl.id,pp.product_name_and_color, sl.name,pp.id;
        # )
        # from_ = f"""
        #     product_product as pp
        #     LEFT JOIN product_template pt on pp.product_tmpl_id = pt.id
        #     LEFT JOIN stock_move_line sml ON sml.product_id = pp.id
        #         AND sml.qty_done > 0
        #     INNER JOIN incoming_moves on incoming_moves.location_dest_id = sml.location_id
        #         AND incoming_moves.product_id = sml.product_id
        #         AND incoming_moves.product = pp.product_name_and_color
        #     INNER JOIN outgoing_moves ON outgoing_moves.location_id = sml.location_id
        #         AND outgoing_moves.product_id = sml.product_id
        #         AND outgoing_moves.product = pp.product_name_and_color
        #     {from_clause}
        # """
        # groupby_ = (
        #     """
        #     pp.id,
        #     pt.categ_id,
        #     pt.brand_id,
        #     pt.product_seasons_id,
        #     pt.product_family_id,
        #     pt.product_material_id,
        #     pp.product_name_and_color,
        #     CASE WHEN sl.usage = 'internal'
        #         THEN sml.location_dest_id
        #         WHEN sl.id = cl.id
        #         THEN sml.location_id
        #         ELSE 0
        #     END as location_id,
        #     sml.company_id,
        #     sml.date,
        #     sml.id
        #     %s
        # """
        #     % groupby
        # )
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

        # _logger.info("%s (SELECT %s FROM %s WHERE %s GROUP BY %s)" % (
        #     with_,
        #     select_,
        #     from_,
        #     where_,
        #     groupby_,
        # ))
        
        query1= "(SELECT %s FROM %s WHERE %s GROUP BY %s)" % (
            # with_,
            select_,
            from_,
            where_,
            groupby_,
        )
        select_2 = """
            mq.id as id,
            mq.product_id as product_id,
            mq.categ_id as categ_id,
            mq.brand_id as brand_id,
            mq.product_seasons_id as product_seasons_id,
            mq.product_family_id as product_family_id,
            mq.product_material_id as product_material_id,
            mq.product_name_and_color as product_name_and_color,
            mq.location_id as location_id,
            mq.company_id as company_id,
            mq.qty_received as qty_received,
            mq.qty_sold as qty_sold,
            (mq.qty_received - mq.qty_sold) as balance,
            mq.date as date,
            mq.move_line_id as move_line_id            
        """
        from_2 = f"""
        {query1} as mq
        INNER JOIN stock_quant sq on sq.location_id = mq.location_id
        """
        groupby_2 = f"""
            mq.id,
            mq.product_id,
            mq.categ_id,
            mq.brand_id,
            mq.product_seasons_id,
            mq.product_family_id,
            mq.product_material_id,
            mq.product_name_and_color,
            mq.location_id,
            mq.company_id,
            mq.qty_received,
            mq.qty_sold,
            mq.date,
            (mq.qty_received - mq.qty_sold),
            mq.move_line_id
        """


        return "%s (SELECT %s FROM %s GROUP BY %s)" % (
            with_,
            select_2,
            from_2,
            groupby_2,
        )

    def init(self):
        # self._table = sale_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            """CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query())
        )

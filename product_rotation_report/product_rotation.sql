/* 
Nombre Funcion: product_rotation
Parametros:
	- p_date_from: Fecha rango inferior
	- p_date_to: Fecha rango superior
	- p_product_id: id de producto para particular o null

Descripcion: Rotacion de productos

Test

select *
   from product_rotation_report() as (id integer, partner_id integer, company_id integer, company varchar, default_code varchar, product_id integer, product varchar,
			 product_variant varchar, product_template_id integer, categ_id integer, categ varchar, brand_id integer, brand varchar, product_season_id integer, 
			 product_season varchar, product_family_id integer,product_family varchar, product_material_id integer, product_material varchar, 
			 location_id integer, location_name varchar, date_order date, available decimal(12,2), sold decimal(12,2))
*/

--drop view product_rotation_report(date,date)
--drop function product_rotation_report(date,date)
create or replace function product_rotation_report(p_date_from date default null, p_date_to date default null)
returns setof record as $$

declare out_file varchar;
	boleta record;
begin

drop table if exists tmp_records;
create table tmp_records(partner_id integer, company_id integer, company varchar, default_code varchar, product_id integer, product varchar,
			 product_variant varchar, product_template_id integer, categ_id integer, categ varchar, brand_id integer, brand varchar, product_season_id integer, 
			 product_season varchar, product_family_id integer,product_family varchar, product_material_id integer, product_material varchar);

insert into tmp_records(partner_id, company_id, company, default_code, product_id, product, product_variant, product_template_id, categ_id, categ, brand_id, 
			brand, product_season_id, product_season, product_family_id, product_family, product_material_id, product_material)

select c.partner_id as "partner_id" --company
     , c.id as "company_id"
     , c.name as "company" 
     , pp.default_code as "default_code"
     , pp.id as "product_id"
     , pt.name as "product"
     , (select string_agg(pa.name || ':' || pav.name, ' - ') as variant
	  from (select unnest(string_to_array(ppv.combination_indices,','))::integer as "product_attribute_value_id"
		  from product_product ppv 
		 where ppv.id = pp.id
		) ppvi 
	 inner join product_template_attribute_value ptav
	    on ptav.id = ppvi.product_attribute_value_id
	 inner join product_attribute pa
	    on pa.id = ptav.attribute_id
	 inner join product_attribute_value pav
	    on pav.id = ptav.product_attribute_value_id  
       ) as "product_variant"     
     , pt.id as "product_template_id"
     , pc.id as "categ_id"
     , pc.name as "categ"
     , pb.id as "brand_id"
     , pb.name as "brand"
     , ps.id as "product_season_id"
     , ps.description as "product_season"     
     , pf.id as "product_family_id"
     , pf.description as "product_family"
     , pm.id as "product_material_id"
     , pm.description as "product_material"
  from product_product pp 
 inner join product_template pt
    on pt.id = pp.product_tmpl_id
 inner join product_template_res_company_rel ptc
    on ptc.product_template_id = pt.id
  inner join res_company c
    on c.id = ptc.res_company_id
 inner join product_category pc
    on pc.id = pt.categ_id
 inner join product_seasons ps
    on ps.id = pt.product_seasons_id
 inner join product_family pf
    on pf.id = pt.product_family_id
 inner join product_material pm
    on pm.id = pt.product_material_id
 inner join product_brand pb
    on pb.id = pt.brand_id
 where pt.type = 'product'
 order by c.name, pt.name, product_variant;

--Movimientos de productos

drop table if exists tmp_oe;
create table tmp_oe(company_id integer, date_oe date, stock_location_id integer, stock_location_name varchar, stock_location_usage varchar, product_id integer, qty_done decimal(12,2));

insert into tmp_oe(company_id, date_oe, stock_location_id, stock_location_name, stock_location_usage, product_id, qty_done)

select sm.company_id "company_id"
     , sml.date as "date_oe"
     , sl.id as "stock_location_id"
     , sl.complete_name as "stock_location_name"
     , sl.usage "stock_location_usage"     
     , sml.product_id as "product_id"
     , sml.qty_done as "qty_done"
  from stock_move_line sml
 inner join stock_move sm    
    on sm.id = sml.move_id
 inner join stock_location sl
    on sl.id = sml.location_dest_id 
 inner join tmp_records t
    on t.product_id = sml.product_id
   and t.company_id = sm.company_id
 where sml.state = 'done'
   and ((to_char(sml.date,'YYYYMMDD') between to_char(p_date_from,'YYYYMMDD') and to_char(p_date_to,'YYYYMMDD')
	 and p_date_from is not null and p_date_to is not null
        ) or (p_date_from is null and p_date_to is null)
       );

--calculos disponibilidad y ventas, stock actual a hoy

drop table if exists tmp_result;
create table tmp_result(id integer, partner_id integer, company_id integer, company varchar, default_code varchar, product_id integer, product varchar,
			 product_variant varchar, product_template_id integer, categ_id integer, categ varchar, brand_id integer, brand varchar, product_season_id integer, 
			 product_season varchar, product_family_id integer,product_family varchar, product_material_id integer, product_material varchar, 
			 location_id integer, location_name varchar, date_order date, available decimal(12,2), sold decimal(12,2));

insert into tmp_result(id, partner_id, company_id, company, default_code, product_id, product, product_variant, product_template_id, categ_id, categ, brand_id, 
			brand, product_season_id, product_season, product_family_id, product_family, product_material_id, product_material,
			location_id, location_name, date_order, available, sold)

select ROW_NUMBER() OVER() as "id" 
     , t.partner_id
     , t.company_id
     , t.company
     , t.default_code
     , t.product_id
     , t.product
     , t.product_variant
     , t.product_template_id
     , t.categ_id
     , t.categ
     , t.brand_id
     , t.brand
     , t.product_season_id
     , t.product_season
     , t.product_family_id
     , t.product_family
     , t.product_material_id
     , t.product_material
     , o.stock_location_id as "location_id"
     , o.stock_location_name as "location_name"
     , o.date_oe as "date_order"
     , sum(o.qty_done * case when o.stock_location_usage <> 'customer' then 1.00 
                             else 0.00 
                         end) as "available"
     , sum(o.qty_done * case when o.stock_location_usage = 'customer' then 1.00 
                             else 0.00 
                         end) as "sold"
  from tmp_records t
 inner join tmp_oe o
    on o.company_id = t.company_id
   and o.product_id = t.product_id
 group by t.partner_id
     , t.company_id
     , t.company
     , t.default_code
     , t.product_id
     , t.product
     , t.product_variant
     , t.product_template_id
     , t.categ_id
     , t.categ
     , t.brand_id
     , t.brand
     , t.product_season_id
     , t.product_season
     , t.product_family_id
     , t.product_family
     , t.product_material_id
     , t.product_material
     , o.stock_location_id
     , o.stock_location_name
     , o.date_oe; 

--retorno del resultado
return query
select *
 from tmp_result;

drop table if exists tmp_records;
drop table if exists tmp_oe;
drop table if exists tmp_result;
end
$$
language 'plpgsql' volatile;
----------------------------------------------------------------------------------------
/* 
Nombre Funcion: product_rotation
Parametros:
	- p_date_from: Fecha rango inferior
	- p_date_to: Fecha rango superior

Descripcion: Rotacion de productos

Test

select *
   from product_rotation_report() as (id integer, partner_id integer, company_id integer, company varchar, default_code varchar, product_id integer, product_and_color varchar,
			 product_color varchar, product_size varchar, product_template_id integer, categ_id integer, categ varchar, brand_id integer, brand varchar, product_season_id integer, 
			 product_season varchar, product_family_id integer,product_family varchar, product_material_id integer, product_material varchar, 
			 location_id integer, location_name varchar, date_order date, available decimal(12,2), sold decimal(12,2))
*/

--drop function product_rotation_report(date,date)
create or replace function product_rotation_report(p_date_from date default null, p_date_to date default null)
returns setof record as $$

begin

--Movimientos de productos

drop table if exists tmp_oe;
create table tmp_oe(company_id integer, date_oe date, location_id integer, location_name varchar, location_usage varchar,
		    location_dest_id integer, location_dest_name varchar, location_dest_usage varchar, 
		    product_id integer, qty_done decimal(12,2));

insert into tmp_oe(company_id, date_oe, location_id, location_name, location_usage, location_dest_id, location_dest_name, location_dest_usage, product_id, qty_done)

select sm.company_id "company_id"
     , sml.date as "date_oe"
     , l.id as "location_id"
     , l.complete_name as "location_name"
     , l.usage "location_usage"     
     , ld.id as "location_dest_id"
     , ld.complete_name as "location_dest_name"
     , ld.usage "location_dest_usage"          
     , sml.product_id as "product_id"
     , sml.qty_done as "qty_done"
  from stock_move_line sml
 inner join stock_move sm    
    on sm.id = sml.move_id
 inner join stock_location l
    on l.id = sml.location_id     
 inner join stock_location ld
    on ld.id = sml.location_dest_id 
 where sml.state = 'done'
   and ((to_char(sml.date,'YYYYMMDD') between to_char(p_date_from,'YYYYMMDD') and to_char(p_date_to,'YYYYMMDD')
	 and p_date_from is not null and p_date_to is not null
        ) or (p_date_from is null and p_date_to is null)
       );


drop table if exists tmp_records;
create table tmp_records(partner_id integer, company_id integer, company varchar, default_code varchar, product_id integer, product varchar,
			 product_color varchar, product_size varchar, product_template_id integer, categ_id integer, categ varchar, brand_id integer, brand varchar, product_season_id integer, 
			 product_season varchar, product_family_id integer,product_family varchar, product_material_id integer, product_material varchar);

insert into tmp_records(partner_id, company_id, company, default_code, product_id, product, product_color, product_size, product_template_id, categ_id, categ, brand_id, 
			brand, product_season_id, product_season, product_family_id, product_family, product_material_id, product_material)

select distinct c.partner_id as "partner_id" --company
     , c.id as "company_id"
     , c.name as "company" 
     , pp.default_code as "default_code"
     , pp.id as "product_id"
     , pt.name as "product"
     , (select pav.name as color
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
	 where pa.display_type = 'color' 
       ) as "product_color"     
     , (select pav.name as size
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
	 where pa.display_type = 'size' 
       ) as "product_size"   
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
  from tmp_oe t
 inner join product_product pp 
    on pp.id = t.product_id
 inner join product_template pt
    on pt.id = pp.product_tmpl_id
 inner join res_company c
    on c.id = t.company_id 
  left join product_category pc
    on pc.id = pt.categ_id
  left join product_seasons ps
    on ps.id = pt.product_seasons_id
  left join product_family pf
    on pf.id = pt.product_family_id
  left join product_material pm
    on pm.id = pt.product_material_id
  left join product_brand pb
    on pb.id = pt.brand_id
 where pt.type = 'product'
 order by c.name, pt.name, product_color, product_size;

--calculos disponibilidad y ventas, stock actual a hoy

drop table if exists tmp_result;
create table tmp_result(id integer, partner_id integer, company_id integer, company varchar, default_code varchar, product_id integer, product varchar,
			 product_color varchar, product_size varchar, product_template_id integer, categ_id integer, categ varchar, brand_id integer, brand varchar, product_season_id integer, 
			 product_season varchar, product_family_id integer,product_family varchar, product_material_id integer, product_material varchar, 
			 location_id integer, location_name varchar, date_order date, available decimal(12,2), sold decimal(12,2));

insert into tmp_result(id, partner_id, company_id, company, default_code, product_id, product, product_color, product_size, product_template_id, categ_id, categ, brand_id, 
			brand, product_season_id, product_season, product_family_id, product_family, product_material_id, product_material,
			location_id, location_name, date_order, available, sold)

--Todas las locaciones de stock de origen + todas las locaciones de stock de destino
select ROW_NUMBER() OVER() as "id" 
     , t.partner_id
     , t.company_id
     , t.company
     , t.default_code
     , t.product_id
     , t.product || coalesce(' - ' || t.product_color,'') as "product"
     , t.product_color
     , t.product_size
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
     , o.location_dest_id as "location_id"
     , o.location_dest_name as "location_name"
     , o.date_oe as "date_order"
     , sum(o.qty_done * case when o.location_dest_usage <> 'customer' then 1.00 
                             else 0.00 
                         end) as "available"
     , sum(o.qty_done * case when o.location_dest_usage = 'customer' then 1.00 
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
     , t.product_color
     , t.product_size
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
     , o.location_dest_id
     , o.location_dest_name
     , o.date_oe

union all

select ROW_NUMBER() OVER() as "id" 
     , t.partner_id
     , t.company_id
     , t.company
     , t.default_code
     , t.product_id
     , t.product || coalesce(' - ' || t.product_color,'') as "product"
     , t.product_color
     , t.product_size
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
     , o.location_id as "location_id"
     , o.location_name as "location_name"
     , o.date_oe as "date_order"
     , sum(o.qty_done * case when o.location_usage = 'customer' then 1.00 
                             else 0.00 
                         end) as "available"
     , sum(o.qty_done * case when o.location_usage <> 'customer' then 1.00 
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
     , t.product_color
     , t.product_size
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
     , o.location_id
     , o.location_name
     , o.date_oe;     

--retorno del resultado
return query
select t.id
     , t.partner_id
     , t.company_id
     , t.company
     , t.default_code
     , t.product_id
     , t.product as "product_and_color"
     , t.product_color
     , t.product_size
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
     , t.location_id
     , t.location_name
     , t.date_order
     --al disponible le restamos lo vendido (o que salio)
     , (sum(t.available) - sum(t.sold))::decimal(12,2) as "available"
     , sum(t.sold)::decimal(12,2) as "sold"
 from tmp_result t
 inner join stock_location l
    on l.id = t.location_id   
   and l.usage = 'internal' 
group by t.id
     , t.partner_id
     , t.company_id
     , t.company
     , t.default_code
     , t.product_id
     , t.product
     , t.product_color
     , t.product_size
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
     , t.location_id
     , t.location_name
     , t.date_order
 order by t.product_color
     , t.company
     , t.product_size
     , t.categ
     , t.brand
     , t.product_season
     , t.product_family
     , t.product_material
     , t.location_name
     , t.date_order;
     
drop table if exists tmp_records;
drop table if exists tmp_oe;
drop table if exists tmp_result;
end
$$
language 'plpgsql' volatile;
----------------------------------------------------------------------------------------
select concat(sku_code, '_', coalesce(store_id, '-1'), '_', coalesce(channel_id, '-1'), case when length(sale_date) > 10 then concat('_', substring(sale_date, 12)) else '' end) as sku_id,pre_target_dimension_id as Granu,category_code_1 as cate1,category_code_2 as cate2,category_code_3 as cate3,price,sale,case when length(sale_date) > 10 then substring(sale_date, 1, 10) else sale_date end as dt, uv, pv, cast(date_format(case when length(sale_date) > 10 then substring(sale_date, 1, 10) else sale_date end,'u') as int)  as weekday , pre_target_dimension_id, dynamic_dims from app.app_saas_sfs_model_input where tenant_id = {Tenant_id} and dt = '{sfs_dt}' and sale_date >='{start_date}' and sale_date <= '{end_date}' and sku_code like '1172%'
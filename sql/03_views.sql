-- Flat, denormalized view for Power BI import / DirectQuery
CREATE OR REPLACE VIEW salesops.vw_sales_flat AS
SELECT
    f.sale_key,
    f.order_id,
    d.full_date,
    d.year,
    d.quarter,
    d.month_name,
    c.customer_id,
    c.customer_name,
    c.segment,
    r.region_name,
    r.sales_manager,
    p.product_name,
    p.category,
    p.sub_category,
    f.quantity,
    f.unit_price,
    f.discount,
    f.sales_amount,
    f.profit
FROM salesops.fact_sales f
JOIN salesops.dim_date     d ON f.date_key     = d.date_key
JOIN salesops.dim_customer c ON f.customer_key = c.customer_key
JOIN salesops.dim_product  p ON f.product_key  = p.product_key
JOIN salesops.dim_region   r ON f.region_key   = r.region_key;

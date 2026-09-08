# Power BI Data Model

## Source
Connect via **Get Data → PostgreSQL database**:
- Server: `localhost:5432` (or your deployed host)
- Database: `salesops`
- Mode: Import (or DirectQuery if the fact table grows large)

Import these tables/view from schema `salesops`:
- `dim_date`
- `dim_region`
- `dim_customer`
- `dim_product`
- `fact_sales`

(`vw_sales_flat` is kept as a debugging/QA view — not imported into the model, since Power BI does its own star-schema relationships.)

## Relationships
Star schema, all 1-to-many from dimension → fact, single direction:

| From (dimension)      | To (fact)             | Cardinality | Cross-filter |
|------------------------|------------------------|-------------|--------------|
| dim_date[date_key]      | fact_sales[date_key]     | 1:*         | Single       |
| dim_customer[customer_key] | fact_sales[customer_key] | 1:*     | Single       |
| dim_product[product_key]  | fact_sales[product_key]  | 1:*     | Single       |
| dim_region[region_key]    | fact_sales[region_key]   | 1:*     | Single       |

## Mark as Date Table
Mark `dim_date[full_date]` as the official Date Table (Table tools → Mark as date table) so time-intelligence DAX functions work correctly.

## Hide Foreign Keys
Hide `*_key` columns on `fact_sales` from Report View once relationships are built — they're modeling-only, not report-facing.

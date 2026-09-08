# Architecture

```text
data/raw/orders.csv
│
▼
etl/extract.py ──► validate columns, normalize headers
│
▼
etl/transform.py ──► clean rows, build star-schema DataFrames
│ (dim_date, dim_region, dim_customer,
│ dim_product, fact_sales)
▼
etl/load.py ──► write to PostgreSQL (salesops schema)
│
▼
PostgreSQL (Docker) ──► Power BI (Import mode, Get Data → PostgreSQL)
│
▼
Data model + DAX + RLS + report pages
│
▼
Power BI Service (published, scheduled refresh)
```


## Why this shape
- **Star schema in Postgres, not raw CSV import into Power BI** — mirrors how this is actually done in industry, and lets DAX time-intelligence functions and RLS work correctly against a proper dimensional model.
- **ETL is tested independently of Power BI** (`tests/`) — the ETL correctness doesn't depend on opening Power BI Desktop, so it's CI-friendly.
- **`vw_sales_flat`** exists purely for manual QA (quick `SELECT *` sanity checks) — it is not imported into the Power BI model, which uses the real star schema and its relationships.

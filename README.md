# salesops-analytics

End-to-end sales & customer analytics pipeline — a star-schema PostgreSQL
data model, a tested Python/pandas ETL layer, and an interactive Power BI
dashboard with DAX measures, drill-through navigation, and row-level
security.

## Stack
Python (pandas, SQLAlchemy) · PostgreSQL · Docker Compose · Power BI (DAX, RLS)

## Architecture
See [`docs/architecture.md`](docs/architecture.md).

## Setup

1. Copy `.env.example` to `.env` and adjust if needed.
2. Start PostgreSQL: `docker compose up -d`
3. Place the source data (Kaggle "Superstore Dataset Final") at `data/raw/orders.csv`.
4. Install dependencies: `pip install -r requirements.txt`
5. Run the pipeline: `python -m etl.pipeline`

## Verified results

The pipeline has been run end-to-end against the public Superstore dataset
(9,994 raw rows):

| Table            | Rows loaded |
|------------------|-------------|
| `dim_region`     | 4           |
| `dim_customer`   | 793         |
| `dim_product`    | 1,862       |
| `dim_date`       | 1,237       |
| `fact_sales`     | 9,986       |

8 invalid/duplicate rows were identified and dropped during cleaning.

Test suite, type-checking, and linting all pass clean:

```bash
pytest -v → 6 passed
mypy etl/ tests/ → Success: no issues found in 9 source files
ruff check → All checks passed!
```


## Power BI
Connection details, data model, DAX measures, RLS setup, and report page
layout are documented in [`powerbi/`](powerbi/).

## Status
- ETL pipeline, schema, and tests: **complete and verified** (see results above)

## License
MIT — see [LICENSE](LICENSE).

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
3. Place the source data at `data/raw/orders.csv` (see `data/raw/README.md`).
4. Install dependencies and run the pipeline (see below).

## Power BI
Connection details, data model, DAX measures, RLS setup, and report page
layout are documented in [`powerbi/`](powerbi/).

## Status
ETL pipeline and schema: complete and tested.
Power BI report: in progress.

## License
MIT — see [LICENSE](LICENSE).

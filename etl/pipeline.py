"""Pipeline orchestration: extract -> transform -> load, runnable as a script."""

from __future__ import annotations

from etl.config import load_db_config, load_path_config
from etl.extract import extract_orders
from etl.load import get_engine, load_star_schema
from etl.transform import (
    build_dim_customer,
    build_dim_date,
    build_dim_product,
    build_dim_region,
    build_fact_sales,
    clean_orders,
)


def run_pipeline() -> None:
    paths = load_path_config()
    db_config = load_db_config()

    print("[pipeline] extracting raw orders...")
    raw = extract_orders(paths.raw_orders_csv)

    print("[pipeline] cleaning...")
    clean = clean_orders(raw)

    print("[pipeline] building dimensions...")
    dim_region = build_dim_region(clean)
    dim_customer = build_dim_customer(clean, dim_region)
    dim_product = build_dim_product(clean)
    dim_date = build_dim_date(clean)

    print("[pipeline] building fact table...")
    fact_sales = build_fact_sales(clean, dim_date, dim_customer, dim_product, dim_region)

    paths.processed_dir.mkdir(parents=True, exist_ok=True)
    fact_sales.to_csv(paths.processed_dir / "fact_sales.csv", index=False)

    print("[pipeline] loading into PostgreSQL...")
    engine = get_engine(db_config)
    load_star_schema(engine, dim_date, dim_region, dim_customer, dim_product, fact_sales)

    print("[pipeline] done.")


if __name__ == "__main__":
    run_pipeline()

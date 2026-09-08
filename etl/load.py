"""Load: write star-schema DataFrames into PostgreSQL."""

from __future__ import annotations

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from etl.config import DBConfig


def get_engine(db_config: DBConfig) -> Engine:
    return create_engine(db_config.sqlalchemy_url)


def load_table(df: pd.DataFrame, table_name: str, engine: Engine, if_exists: str = "append") -> None:
    df.to_sql(
        table_name,
        engine,
        schema="salesops",
        if_exists=if_exists,
        index=False,
        method="multi",
        chunksize=1000,
    )
    print(f"[load] wrote {len(df)} rows -> salesops.{table_name}")


def load_star_schema(
    engine: Engine,
    dim_date: pd.DataFrame,
    dim_region: pd.DataFrame,
    dim_customer: pd.DataFrame,
    dim_product: pd.DataFrame,
    fact_sales: pd.DataFrame,
) -> None:
    # Order matters: dimensions before the fact table (FK constraints).
    load_table(dim_region, "dim_region", engine, if_exists="append")
    load_table(dim_customer, "dim_customer", engine, if_exists="append")
    load_table(dim_product, "dim_product", engine, if_exists="append")
    load_table(dim_date, "dim_date", engine, if_exists="append")
    load_table(fact_sales, "fact_sales", engine, if_exists="append")

"""Transformation: clean raw orders and shape them into star-schema tables."""

from __future__ import annotations

import pandas as pd


def clean_orders(df: pd.DataFrame) -> pd.DataFrame:
    """Type-cast, de-duplicate, and drop invalid rows."""
    df = df.copy()

    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df["sales"] = pd.to_numeric(df["sales"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["discount"] = pd.to_numeric(df["discount"], errors="coerce").fillna(0.0)
    df["profit"] = pd.to_numeric(df["profit"], errors="coerce")

    before = len(df)
    df = df.dropna(subset=["order_date", "sales", "quantity", "order_id", "customer_id"])
    df = df.drop_duplicates(subset=["order_id", "product_id", "customer_id"])
    dropped = before - len(df)
    if dropped:
        print(f"[transform] dropped {dropped} invalid/duplicate rows")

    df = df[(df["sales"] > 0) & (df["quantity"] > 0)]
    return df.reset_index(drop=True)


def build_dim_region(df: pd.DataFrame) -> pd.DataFrame:
    regions = df[["region"]].drop_duplicates().reset_index(drop=True)
    regions = regions.rename(columns={"region": "region_name"})
    # sales_manager is illustrative placeholder data, assigned round-robin
    managers = ["Aditi Rao", "Vikram Shah", "Priya Nair", "Rohan Mehta"]
    regions["sales_manager"] = [managers[i % len(managers)] for i in range(len(regions))]
    regions.insert(0, "region_key", range(1, len(regions) + 1))
    return regions


def build_dim_customer(df: pd.DataFrame, dim_region: pd.DataFrame) -> pd.DataFrame:
    cust = (
        df[["customer_id", "customer_name", "segment", "city", "state", "region"]]
        .drop_duplicates(subset=["customer_id"])
        .reset_index(drop=True)
    )
    cust = cust.merge(
        dim_region, left_on="region", right_on="region_name", how="left"
    ).drop(columns=["region", "region_name", "sales_manager"])
    cust.insert(0, "customer_key", range(1, len(cust) + 1))
    return cust


def build_dim_product(df: pd.DataFrame) -> pd.DataFrame:
    prod = (
        df[["product_id", "product_name", "category", "sub_category"]]
        .drop_duplicates(subset=["product_id"])
        .reset_index(drop=True)
    )
    prod.insert(0, "product_key", range(1, len(prod) + 1))
    return prod


def build_dim_date(df: pd.DataFrame) -> pd.DataFrame:
    dates = df[["order_date"]].drop_duplicates().rename(columns={"order_date": "full_date"})
    dates["date_key"] = dates["full_date"].dt.strftime("%Y%m%d").astype(int)
    dates["year"] = dates["full_date"].dt.year
    dates["quarter"] = dates["full_date"].dt.quarter
    dates["month"] = dates["full_date"].dt.month
    dates["month_name"] = dates["full_date"].dt.month_name()
    dates["day"] = dates["full_date"].dt.day
    dates["day_of_week"] = dates["full_date"].dt.day_name()
    dates["is_weekend"] = dates["full_date"].dt.dayofweek.isin([5, 6])
    return dates[
        ["date_key", "full_date", "year", "quarter", "month",
         "month_name", "day", "day_of_week", "is_weekend"]
    ].sort_values("date_key").reset_index(drop=True)


def build_fact_sales(
    df: pd.DataFrame,
    dim_date: pd.DataFrame,
    dim_customer: pd.DataFrame,
    dim_product: pd.DataFrame,
    dim_region: pd.DataFrame,
) -> pd.DataFrame:
    fact = df.copy()
    fact["date_key"] = fact["order_date"].dt.strftime("%Y%m%d").astype(int)

    fact = fact.merge(dim_customer[["customer_id", "customer_key", "region_key"]],
                       on="customer_id", how="left")
    fact = fact.merge(dim_product[["product_id", "product_key"]], on="product_id", how="left")

    fact["unit_price"] = (fact["sales"] / fact["quantity"]).round(2)

    out = fact[
        ["order_id", "date_key", "customer_key", "product_key", "region_key",
         "quantity", "unit_price", "discount", "sales", "profit"]
    ].rename(columns={"sales": "sales_amount"})

    return out.reset_index(drop=True)

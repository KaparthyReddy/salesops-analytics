"""Unit tests for etl/transform.py."""

from __future__ import annotations

import pandas as pd
import pytest

from etl.transform import (
    build_dim_customer,
    build_dim_date,
    build_dim_product,
    build_dim_region,
    build_fact_sales,
    clean_orders,
)


@pytest.fixture
def raw_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "order_id": ["O1", "O2", "O2", "O3"],
            "order_date": ["2024-01-05", "2024-01-06", "2024-01-06", "not-a-date"],
            "customer_id": ["C1", "C2", "C2", "C3"],
            "customer_name": ["Alice", "Bob", "Bob", "Cara"],
            "segment": ["Consumer", "Corporate", "Corporate", "Consumer"],
            "city": ["Pune", "Delhi", "Delhi", "Mumbai"],
            "state": ["MH", "DL", "DL", "MH"],
            "region": ["West", "North", "North", "West"],
            "product_id": ["P1", "P2", "P2", "P3"],
            "product_name": ["Chair", "Desk", "Desk", "Lamp"],
            "category": ["Furniture", "Furniture", "Furniture", "Furniture"],
            "sub_category": ["Chairs", "Desks", "Desks", "Lamps"],
            "sales": [100.0, 250.0, 250.0, 40.0],
            "quantity": [2, 1, 1, 1],
            "discount": [0.1, 0.0, 0.0, 0.0],
            "profit": [20.0, 30.0, 30.0, -5.0],
        }
    )


def test_clean_orders_drops_invalid_dates_and_duplicates(raw_df: pd.DataFrame) -> None:
    cleaned = clean_orders(raw_df)
    # O3 has an invalid date and should be dropped; the duplicate O2 row collapses to one.
    assert "O3" not in cleaned["order_id"].values
    assert len(cleaned[cleaned["order_id"] == "O2"]) == 1
    assert len(cleaned) == 2


def test_build_dim_region_assigns_unique_keys(raw_df: pd.DataFrame) -> None:
    cleaned = clean_orders(raw_df)
    dim_region = build_dim_region(cleaned)
    assert set(dim_region["region_name"]) == {"West", "North"}
    assert dim_region["region_key"].is_unique


def test_build_fact_sales_computes_unit_price(raw_df: pd.DataFrame) -> None:
    cleaned = clean_orders(raw_df)
    dim_region = build_dim_region(cleaned)
    dim_customer = build_dim_customer(cleaned, dim_region)
    dim_product = build_dim_product(cleaned)
    dim_date = build_dim_date(cleaned)

    fact = build_fact_sales(cleaned, dim_date, dim_customer, dim_product, dim_region)

    row_o1 = fact[fact["order_id"] == "O1"].iloc[0]
    assert row_o1["unit_price"] == pytest.approx(50.0)  # 100.0 sales / 2 qty
    assert set(fact.columns) == {
        "order_id", "date_key", "customer_key", "product_key", "region_key",
        "quantity", "unit_price", "discount", "sales_amount", "profit",
    }

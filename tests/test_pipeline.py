"""Integration-style tests for the extract step and pipeline wiring.

These do not require a live database - they validate the
extract/transform boundary and error handling that pipeline.py relies on.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from etl.extract import extract_orders


def test_extract_orders_raises_on_missing_file(tmp_path: Path) -> None:
    missing_path = tmp_path / "does_not_exist.csv"
    with pytest.raises(FileNotFoundError):
        extract_orders(missing_path)


def test_extract_orders_raises_on_missing_columns(tmp_path: Path) -> None:
    bad_csv = tmp_path / "orders.csv"
    pd.DataFrame({"Order ID": ["O1"], "Sales": [100]}).to_csv(bad_csv, index=False)

    with pytest.raises(ValueError, match="Missing required columns"):
        extract_orders(bad_csv)


def test_extract_orders_normalizes_column_names(tmp_path: Path) -> None:
    good_csv = tmp_path / "orders.csv"
    pd.DataFrame(
        {
            "Order ID": ["O1"],
            "Order Date": ["2024-01-05"],
            "Customer ID": ["C1"],
            "Customer Name": ["Alice"],
            "Segment": ["Consumer"],
            "City": ["Pune"],
            "State": ["MH"],
            "Region": ["West"],
            "Product ID": ["P1"],
            "Product Name": ["Chair"],
            "Category": ["Furniture"],
            "Sub-Category": ["Chairs"],
            "Sales": [100.0],
            "Quantity": [2],
            "Discount": [0.1],
            "Profit": [20.0],
        }
    ).to_csv(good_csv, index=False)

    df = extract_orders(good_csv)
    assert "order_id" in df.columns
    assert "sub_category" in df.columns
    assert len(df) == 1

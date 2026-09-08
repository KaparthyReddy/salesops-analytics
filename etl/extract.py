"""Extraction: read the raw Superstore-style CSV into a DataFrame."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = [
    "order_id",
    "order_date",
    "customer_id",
    "customer_name",
    "segment",
    "city",
    "state",
    "region",
    "product_id",
    "product_name",
    "category",
    "sub_category",
    "sales",
    "quantity",
    "discount",
    "profit",
]


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )
    return df


def extract_orders(csv_path: Path) -> pd.DataFrame:
    """Read the raw orders CSV and validate its shape.

    Raises FileNotFoundError if csv_path does not exist, and ValueError
    if any required column is missing after normalization.
    """
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Raw orders CSV not found at {csv_path}. "
            "See data/raw/README.md for the expected file."
        )

    df = pd.read_csv(csv_path, encoding="latin-1")
    df = _normalize_columns(df)

    missing = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns in raw data: {sorted(missing)}")

    return df[REQUIRED_COLUMNS].copy()

"""Environment-driven configuration for the ETL pipeline."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class DBConfig:
    host: str
    port: int
    user: str
    password: str
    database: str

    @property
    def sqlalchemy_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.database}"
        )


@dataclass(frozen=True)
class PathConfig:
    raw_orders_csv: Path
    processed_dir: Path


def load_db_config() -> DBConfig:
    return DBConfig(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=int(os.getenv("POSTGRES_PORT", "5432")),
        user=os.getenv("POSTGRES_USER", "salesops"),
        password=os.getenv("POSTGRES_PASSWORD", "salesops"),
        database=os.getenv("POSTGRES_DB", "salesops"),
    )


def load_path_config() -> PathConfig:
    root = Path(__file__).resolve().parent.parent
    return PathConfig(
        raw_orders_csv=root / "data" / "raw" / "orders.csv",
        processed_dir=root / "data" / "processed",
    )

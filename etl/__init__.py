"""ETL package for salesops-analytics.

Extracts raw order-level CSV data, transforms it into the star-schema
shape defined in sql/01_schema.sql, and loads it into PostgreSQL.
"""

__version__ = "0.1.0"

-- Seed reference dimensions
-- Note: dim_region is intentionally NOT seeded here. The ETL pipeline
-- derives real region names from the source data and owns that table.

-- Populate dim_date for 2022-01-01 through 2026-12-31
INSERT INTO salesops.dim_date (
    date_key, full_date, year, quarter, month, month_name, day, day_of_week, is_weekend
)
SELECT
    CAST(TO_CHAR(d, 'YYYYMMDD') AS INTEGER),
    d::date,
    EXTRACT(YEAR FROM d)::SMALLINT,
    EXTRACT(QUARTER FROM d)::SMALLINT,
    EXTRACT(MONTH FROM d)::SMALLINT,
    TRIM(TO_CHAR(d, 'Month')),
    EXTRACT(DAY FROM d)::SMALLINT,
    TRIM(TO_CHAR(d, 'Day')),
    EXTRACT(ISODOW FROM d) IN (6, 7)
FROM generate_series('2022-01-01'::date, '2026-12-31'::date, interval '1 day') AS d
ON CONFLICT (date_key) DO NOTHING;
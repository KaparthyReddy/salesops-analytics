-- salesops-analytics: star schema
-- Run against PostgreSQL 15+

CREATE SCHEMA IF NOT EXISTS salesops;

CREATE TABLE salesops.dim_date (
    date_key        INTEGER PRIMARY KEY,        -- YYYYMMDD
    full_date       DATE NOT NULL,
    year            SMALLINT NOT NULL,
    quarter         SMALLINT NOT NULL,
    month           SMALLINT NOT NULL,
    month_name      VARCHAR(20) NOT NULL,
    day             SMALLINT NOT NULL,
    day_of_week     VARCHAR(10) NOT NULL,
    is_weekend      BOOLEAN NOT NULL
);

CREATE TABLE salesops.dim_region (
    region_key      SERIAL PRIMARY KEY,
    region_name     VARCHAR(50) NOT NULL,
    sales_manager   VARCHAR(100) NOT NULL
);

CREATE TABLE salesops.dim_customer (
    customer_key    SERIAL PRIMARY KEY,
    customer_id     VARCHAR(20) UNIQUE NOT NULL,
    customer_name   VARCHAR(150) NOT NULL,
    segment         VARCHAR(50) NOT NULL,
    city            VARCHAR(100),
    state           VARCHAR(100),
    region_key      INTEGER REFERENCES salesops.dim_region(region_key)
);

CREATE TABLE salesops.dim_product (
    product_key     SERIAL PRIMARY KEY,
    product_id      VARCHAR(30) UNIQUE NOT NULL,
    product_name    VARCHAR(200) NOT NULL,
    category        VARCHAR(50) NOT NULL,
    sub_category    VARCHAR(50) NOT NULL
);

CREATE TABLE salesops.fact_sales (
    sale_key        BIGSERIAL PRIMARY KEY,
    order_id        VARCHAR(30) NOT NULL,
    date_key        INTEGER NOT NULL REFERENCES salesops.dim_date(date_key),
    customer_key    INTEGER NOT NULL REFERENCES salesops.dim_customer(customer_key),
    product_key     INTEGER NOT NULL REFERENCES salesops.dim_product(product_key),
    region_key      INTEGER NOT NULL REFERENCES salesops.dim_region(region_key),
    quantity        INTEGER NOT NULL,
    unit_price      NUMERIC(10, 2) NOT NULL,
    discount        NUMERIC(4, 3) NOT NULL DEFAULT 0,
    sales_amount    NUMERIC(12, 2) NOT NULL,
    profit          NUMERIC(12, 2) NOT NULL
);

CREATE INDEX idx_fact_sales_date ON salesops.fact_sales(date_key);
CREATE INDEX idx_fact_sales_customer ON salesops.fact_sales(customer_key);
CREATE INDEX idx_fact_sales_product ON salesops.fact_sales(product_key);
CREATE INDEX idx_fact_sales_region ON salesops.fact_sales(region_key);

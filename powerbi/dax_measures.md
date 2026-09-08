# DAX Measures

Create a dedicated measures table (`_Measures`) to keep these organized and separate from imported columns.

## Core measures
```dax
Total Sales = SUM(fact_sales[sales_amount])

Total Profit = SUM(fact_sales[profit])

Profit Margin % = DIVIDE([Total Profit], [Total Sales], 0)

Total Orders = DISTINCTCOUNT(fact_sales[order_id])

Total Quantity = SUM(fact_sales[quantity])
```

## Time intelligence
```dax
Sales PY =
CALCULATE([Total Sales], SAMEPERIODLASTYEAR(dim_date[full_date]))

Sales YoY % =
DIVIDE([Total Sales] - [Sales PY], [Sales PY], 0)

Sales Rolling 3M Avg =
AVERAGEX(
    DATESINPERIOD(dim_date[full_date], MAX(dim_date[full_date]), -3, MONTH),
    [Total Sales]
)
```

## Customer retention
```dax
Active Customers =
DISTINCTCOUNT(fact_sales[customer_key])

Returning Customers =
CALCULATE(
    DISTINCTCOUNT(fact_sales[customer_key]),
    FILTER(
        VALUES(fact_sales[customer_key]),
        CALCULATE(DISTINCTCOUNT(dim_date[year])) > 1
    )
)

Retention Rate % =
DIVIDE([Returning Customers], [Active Customers], 0)
```

## RFM segmentation (customer-level calculated table)
```dax
RFM Table =
ADDCOLUMNS(
    SUMMARIZE(fact_sales, dim_customer[customer_key]),
    "Recency", DATEDIFF(
        CALCULATE(MAX(dim_date[full_date])),
        TODAY(),
        DAY
    ),
    "Frequency", CALCULATE(DISTINCTCOUNT(fact_sales[order_id])),
    "Monetary", CALCULATE(SUM(fact_sales[sales_amount]))
)
```
Bucket Recency/Frequency/Monetary into quintiles (1–5) using `RANKX` or Power Query's `Bin` grouping, then concatenate into an "RFM Score" for segment labels (Champions, At Risk, etc.) in a calculated column.

## Notes
- Every measure uses `SUM`/`CALCULATE`/`DIVIDE` — no hardcoded numbers, so it stays valid once your own data is loaded.
- Wrap ratio measures in `DIVIDE(..., ..., 0)` everywhere to avoid divide-by-zero errors on filtered/empty selections.

# Raw data

Place the source CSV here as `orders.csv`, using the public
**Sample Superstore** dataset (Kaggle: "Superstore Sales Dataset" /
Tableau's standard sample dataset).

Expected columns (case-insensitive, ETL will normalize):
Order ID, Order Date, Customer ID, Customer Name, Segment, City, State,
Region, Product ID, Product Name, Category, Sub-Category, Sales,
Quantity, Discount, Profit

The `etl/extract.py` script reads this file and hands it off to
`transform.py` for cleaning and star-schema shaping.

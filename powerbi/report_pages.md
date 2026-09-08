# Report Pages & Interactivity

## Page 1 — Executive Overview
- KPI cards: Total Sales, Total Profit, Profit Margin %, Sales YoY %
- Line chart: Total Sales by month, with Sales Rolling 3M Avg overlay
- Bar chart: Total Sales by Region
- Slicers: Year, Category

## Page 2 — Regional Drill-Through
- Set up drill-through: right-click a region bar on Page 1 → "Drill through" → lands here filtered to that region
- Table: Sales/Profit by State → City → Customer (drill-down hierarchy)
- Map visual: Sales by City (bubble size = Total Sales)

## Page 3 — Customer Analytics
- Scatter plot: Recency vs Frequency, bubble size = Monetary (from RFM Table)
- Table: Top 20 customers by Total Sales, with Retention Rate %
- Bookmark toggle: "All Customers" vs "At-Risk Segment only" (bookmark + Selection pane to swap filter state on a button click)

## Page 4 — Product Performance
- Treemap: Sales by Category → Sub-Category
- Bar chart: Profit Margin % by Sub-Category (sorted ascending — surfaces loss-making lines first)

## Tooltips
Build one custom tooltip page (small canvas size, e.g. 300×200px) showing Total Sales, Total Profit, and Total Orders for whatever is hovered — set as the report-level tooltip under Format → Tooltip → Report page.

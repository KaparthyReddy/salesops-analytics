# Row-Level Security (RLS)

## Goal
Each sales manager should only see rows for their own region when they open the published report.

## Setup
1. **Modeling → Manage Roles → Create Role**, name it `RegionManager`.
2. On `dim_region`, add a DAX filter expression:
```dax
   [sales_manager] = USERPRINCIPALNAME()
```
3. This propagates to `fact_sales` automatically through the existing `dim_region → fact_sales` relationship (single-direction cross-filter already set in the data model).

## Testing locally
**Modeling → View As Roles** → select `RegionManager` → enter a test email matching one of the `sales_manager` values in `dim_region` (e.g. `aditi.rao@example.com` if you extend the seed data with matching email-style identifiers) → confirm only that region's rows appear across every visual.

## Publishing
After publishing to the Power BI Service:
- **Dataset settings → Security** → add the `RegionManager` role
- Assign actual org email addresses (must match `USERPRINCIPALNAME()`, i.e. their Power BI login) to the role
- Members will now see only their region's data when they open the shared report — no changes to the report itself needed

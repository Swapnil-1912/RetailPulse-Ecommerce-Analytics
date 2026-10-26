"""
Step 1: Load the raw Olist tables, clean them, and build the model tables
(fact_sales + dimensions) that SQL and Power BI will use.
Run:  python notebooks/01_data_cleaning.py
"""
import pandas as pd
from pathlib import Path

RAW = Path("data/raw")
OUT = Path("data/cleaned")
OUT.mkdir(parents=True, exist_ok=True)

# ---------- 1. Load ----------
orders    = pd.read_csv(RAW / "olist_orders_dataset.csv")
customers = pd.read_csv(RAW / "olist_customers_dataset.csv")
items     = pd.read_csv(RAW / "olist_order_items_dataset.csv")
products  = pd.read_csv(RAW / "olist_products_dataset.csv")
payments  = pd.read_csv(RAW / "olist_order_payments_dataset.csv")
reviews   = pd.read_csv(RAW / "olist_order_reviews_dataset.csv")
trans     = pd.read_csv(RAW / "product_category_name_translation.csv")

# ---------- 2. Quick audit ----------
for name, df in [("orders", orders), ("customers", customers), ("items", items),
                 ("products", products), ("payments", payments), ("reviews", reviews)]:
    print(f"{name:10s} rows={len(df):>7,}  dupes={df.duplicated().sum():>5}  "
          f"null cells={df.isnull().sum().sum():>7,}")

# ---------- 3. Clean orders ----------
date_cols = ["order_purchase_timestamp", "order_approved_at",
             "order_delivered_carrier_date", "order_delivered_customer_date",
             "order_estimated_delivery_date"]
for c in date_cols:
    orders[c] = pd.to_datetime(orders[c])

orders = orders.drop_duplicates("order_id")
# Revenue analysis uses delivered orders that have a delivery date
orders = orders[(orders["order_status"] == "delivered") &
                (orders["order_delivered_customer_date"].notna())]

# ---------- 4. Clean products ----------
products = products.merge(trans, on="product_category_name", how="left")
products["product_category"] = (products["product_category_name_english"]
                                .fillna(products["product_category_name"])
                                .fillna("unknown"))
products = products[["product_id", "product_category", "product_weight_g",
                     "product_photos_qty"]]

# ---------- 5. Aggregate payments and reviews to ONE row per order ----------
# (merging them raw would duplicate item rows and inflate revenue)
payments = payments.sort_values("payment_value", ascending=False)
pay_agg = (payments.groupby("order_id")
           .agg(payment_type=("payment_type", "first"),   # main method = largest payment
                payment_installments=("payment_installments", "max"),
                payment_value=("payment_value", "sum"))
           .reset_index())

rev_agg = (reviews.groupby("order_id")["review_score"].mean()
           .round(1).reset_index())

# ---------- 6. Build fact table (grain = one order item) ----------
fact = (items
        .merge(orders, on="order_id", how="inner")
        .merge(customers, on="customer_id", how="left")
        .merge(products, on="product_id", how="left")
        .merge(pay_agg, on="order_id", how="left")
        .merge(rev_agg, on="order_id", how="left"))

# ---------- 7. Feature engineering ----------
fact["revenue"] = fact["price"] + fact["freight_value"]
fact["order_date"] = fact["order_purchase_timestamp"].dt.normalize()
fact["order_month"] = fact["order_purchase_timestamp"].dt.strftime("%Y-%m")
fact["delivery_days"] = (fact["order_delivered_customer_date"]
                         - fact["order_purchase_timestamp"]).dt.days
fact["delay_days"] = (fact["order_delivered_customer_date"]
                      - fact["order_estimated_delivery_date"]).dt.days
fact["is_late"] = (fact["delay_days"] > 0).astype(int)

# Remove impossible values
fact = fact[(fact["price"] > 0) & (fact["delivery_days"] >= 0)]

# The dataset's first/last months are incomplete, trim them
fact = fact[(fact["order_month"] >= "2017-01") & (fact["order_month"] <= "2018-08")]

fact = fact[["order_id", "order_item_id", "customer_unique_id", "customer_state",
             "customer_city", "product_id", "product_category", "seller_id",
             "order_date", "order_month", "price", "freight_value", "revenue",
             "payment_type", "payment_installments", "review_score",
             "delivery_days", "delay_days", "is_late"]]

# ---------- 8. Dimensions ----------
dim_customers = (fact[["customer_unique_id", "customer_city", "customer_state"]]
                 .drop_duplicates("customer_unique_id"))
dim_products = fact[["product_id", "product_category"]].drop_duplicates("product_id")
dim_date = pd.DataFrame({"date": pd.date_range(fact["order_date"].min(),
                                               fact["order_date"].max())})
dim_date["year"] = dim_date["date"].dt.year
dim_date["month_num"] = dim_date["date"].dt.month
dim_date["month_name"] = dim_date["date"].dt.strftime("%b")
dim_date["quarter"] = "Q" + dim_date["date"].dt.quarter.astype(str)
dim_date["weekday"] = dim_date["date"].dt.day_name()

# ---------- 9. Save ----------
fact.to_csv(OUT / "fact_sales.csv", index=False)
dim_customers.to_csv(OUT / "dim_customers.csv", index=False)
dim_products.to_csv(OUT / "dim_products.csv", index=False)
dim_date.to_csv(OUT / "dim_date.csv", index=False)

print(f"\nfact_sales: {len(fact):,} rows | orders: {fact['order_id'].nunique():,} "
      f"| customers: {fact['customer_unique_id'].nunique():,}")
print(f"Total revenue: {fact['revenue'].sum():,.0f}")

"""
Step 3: Customer intelligence: repeat rate, RFM segments, CLV, cohort retention.
Run:  python notebooks/03_rfm_segmentation.py
"""
import pandas as pd
import matplotlib.pyplot as plt

fact = pd.read_csv("data/cleaned/fact_sales.csv", parse_dates=["order_date"])

# Collapse to order level (one row per order)
orders = (fact.groupby(["order_id", "customer_unique_id", "order_date"])
          .agg(revenue=("revenue", "sum")).reset_index())

# ---------- Repeat purchase rate ----------
per_cust = orders.groupby("customer_unique_id")["order_id"].nunique()
print(f"Repeat customer rate: {(per_cust > 1).mean()*100:.2f}%")

# ---------- RFM ----------
snapshot = orders["order_date"].max() + pd.Timedelta(days=1)
rfm = (orders.groupby("customer_unique_id")
       .agg(Recency=("order_date", lambda x: (snapshot - x.max()).days),
            Frequency=("order_id", "nunique"),
            Monetary=("revenue", "sum")))

# Most customers bought once, so rank first to avoid duplicate bin edges
rfm["R"] = pd.qcut(rfm["Recency"].rank(method="first"), 5, labels=[5, 4, 3, 2, 1]).astype(int)
rfm["F"] = pd.qcut(rfm["Frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
rfm["M"] = pd.qcut(rfm["Monetary"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
rfm["RFM_Score"] = rfm["R"] + rfm["F"] + rfm["M"]

def segment(row):
    if row["RFM_Score"] >= 13:                 return "Champions"
    if row["RFM_Score"] >= 10:                 return "Loyal"
    if row["R"] >= 4 and row["F"] <= 2:        return "New / Promising"
    if row["RFM_Score"] >= 7:                  return "Potential Loyalist"
    if row["R"] <= 2 and row["M"] >= 4:        return "Can't Lose Them"
    if row["R"] <= 2:                          return "At Risk / Lost"
    return "Needs Attention"

rfm["Segment"] = rfm.apply(segment, axis=1)

summary = (rfm.groupby("Segment")
           .agg(Customers=("Monetary", "size"),
                Avg_Recency=("Recency", "mean"),
                Avg_Frequency=("Frequency", "mean"),
                Avg_Spend=("Monetary", "mean"),
                Total_Revenue=("Monetary", "sum"))
           .round(2))
summary["Customer_%"] = (summary["Customers"] / summary["Customers"].sum() * 100).round(1)
summary["Revenue_%"] = (summary["Total_Revenue"] / summary["Total_Revenue"].sum() * 100).round(1)
print("\n", summary.sort_values("Total_Revenue", ascending=False))

rfm.reset_index().to_csv("data/cleaned/rfm.csv", index=False)
summary.reset_index().to_csv("data/cleaned/rfm_summary.csv", index=False)

# ---------- Simple CLV (historical) ----------
aov = orders["revenue"].mean()
purchase_freq = orders["order_id"].nunique() / orders["customer_unique_id"].nunique()
print(f"\nAOV={aov:.2f} | purchases/customer={purchase_freq:.3f} | "
      f"historical CLV={aov*purchase_freq:.2f}")

# ---------- Cohort retention ----------
orders["order_month"] = orders["order_date"].dt.to_period("M")
orders["cohort"] = orders.groupby("customer_unique_id")["order_month"].transform("min")
orders["period"] = (orders["order_month"] - orders["cohort"]).apply(lambda x: x.n)

cohort = (orders.groupby(["cohort", "period"])["customer_unique_id"]
          .nunique().unstack(fill_value=0))
retention = cohort.divide(cohort[0], axis=0).round(4)
retention.to_csv("data/cleaned/cohort_retention.csv")

fig, ax = plt.subplots(figsize=(12, 7))
im = ax.imshow(retention.iloc[:, :9] * 100, cmap="Blues", vmax=5, aspect="auto")
ax.set_yticks(range(len(retention))); ax.set_yticklabels(retention.index.astype(str))
ax.set_xlabel("Months since first purchase"); ax.set_title("Cohort Retention % (color cap 5%)")
plt.colorbar(im); plt.tight_layout()
plt.savefig("images/cohort_retention.png", dpi=150)

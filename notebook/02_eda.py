import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams.update({"figure.figsize": (10, 5), "axes.spines.top": False,
                     "axes.spines.right": False, "font.size": 11})
fact = pd.read_csv("data/cleaned/fact_sales.csv", parse_dates=["order_date"])
od = fact.drop_duplicates("order_id")   # one row per order

# KPIs
orders = fact["order_id"].nunique()
revenue = fact["revenue"].sum()
print(f"Revenue: {revenue:,.0f} | Orders: {orders:,} | AOV: {revenue/orders:,.2f}")
print(f"Avg delivery days: {od['delivery_days'].mean():.1f}")
print(f"Late delivery %: {od['is_late'].mean()*100:.1f}")

# 1. Monthly revenue
monthly = fact.groupby("order_month")["revenue"].sum()
ax = monthly.plot(marker="o", color="#2563eb", title="Monthly Revenue")
ax.set_ylabel("Revenue"); plt.xticks(rotation=45); plt.tight_layout()
plt.savefig("images/monthly_revenue.png", dpi=150); plt.close()

# 2. Top 10 categories
top_cat = fact.groupby("product_category")["revenue"].sum().nlargest(10).sort_values()
top_cat.plot(kind="barh", color="#2563eb", title="Top 10 Categories by Revenue")
plt.tight_layout(); plt.savefig("images/top_categories.png", dpi=150); plt.close()

# 3. Revenue by state
state = fact.groupby("customer_state")["revenue"].sum().nlargest(10).sort_values()
state.plot(kind="barh", color="#0d9488", title="Top 10 States by Revenue")
plt.tight_layout(); plt.savefig("images/top_states.png", dpi=150); plt.close()

# 4. Payment types
pay = od["payment_type"].value_counts()
pay.plot(kind="pie", autopct="%1.1f%%", wedgeprops={"width": 0.45},
         title="Payment Method Share"); plt.ylabel("")
plt.tight_layout(); plt.savefig("images/payment_types.png", dpi=150); plt.close()

# 5. Delivery time distribution
od["delivery_days"].clip(upper=60).plot(kind="hist", bins=40, color="#f59e0b",
                                        title="Delivery Time (days, capped at 60)")
plt.tight_layout(); plt.savefig("images/delivery_hist.png", dpi=150); plt.close()

# 6. Late delivery vs review score (key insight)
rev = (od.dropna(subset=["review_score"]).groupby("is_late")["review_score"].mean()
       .rename({0: "On time", 1: "Late"}))
print("\nAvg review score, on-time vs late:")
print(rev.round(2))
rev.plot(kind="bar", color=["#16a34a", "#dc2626"],
         title="Average Review Score: On-time vs Late", rot=0)
plt.ylim(1, 5); plt.tight_layout(); plt.savefig("images/late_vs_review.png", dpi=150)
plt.close()

# 7. Concentration: share of revenue from top 3 categories
share = fact.groupby("product_category")["revenue"].sum().sort_values(ascending=False)
print(f"\nTop 3 categories = {share.head(3).sum()/share.sum()*100:.1f}% of revenue")

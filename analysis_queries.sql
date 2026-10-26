-- Works in SQLite, PostgreSQL and MySQL 8+. Main table: fact_sales (grain = order item)

-- 1. Headline KPIs
SELECT ROUND(SUM(revenue), 2)                     AS total_revenue,
       COUNT(DISTINCT order_id)                   AS total_orders,
       COUNT(DISTINCT customer_unique_id)         AS total_customers,
       ROUND(SUM(revenue) * 1.0 / COUNT(DISTINCT order_id), 2) AS avg_order_value
FROM fact_sales;

-- 2. Top 10 categories by revenue, with % share (window function)
SELECT product_category,
       ROUND(SUM(revenue), 2) AS revenue,
       ROUND(100.0 * SUM(revenue) / SUM(SUM(revenue)) OVER (), 2) AS pct_of_total
FROM fact_sales
GROUP BY product_category
ORDER BY revenue DESC
LIMIT 10;

-- 3. Month-over-month growth (CTE + LAG)
WITH monthly AS (
    SELECT order_month, SUM(revenue) AS revenue
    FROM fact_sales GROUP BY order_month
)
SELECT order_month,
       ROUND(revenue, 2) AS revenue,
       ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY order_month))
             / LAG(revenue) OVER (ORDER BY order_month), 2) AS mom_growth_pct
FROM monthly
ORDER BY order_month;

-- 4. Running (cumulative) revenue
WITH monthly AS (
    SELECT order_month, SUM(revenue) AS revenue FROM fact_sales GROUP BY order_month
)
SELECT order_month, ROUND(revenue, 2) AS revenue,
       ROUND(SUM(revenue) OVER (ORDER BY order_month), 2) AS cumulative_revenue
FROM monthly;

-- 5. Repeat customer rate
WITH cust AS (
    SELECT customer_unique_id, COUNT(DISTINCT order_id) AS n_orders
    FROM fact_sales GROUP BY customer_unique_id
)
SELECT ROUND(100.0 * SUM(CASE WHEN n_orders > 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS repeat_rate_pct
FROM cust;

-- 6. Top 3 categories within each state (RANK per partition)
WITH s AS (
    SELECT customer_state, product_category, SUM(revenue) AS revenue
    FROM fact_sales GROUP BY customer_state, product_category
), ranked AS (
    SELECT *, RANK() OVER (PARTITION BY customer_state ORDER BY revenue DESC) AS rnk FROM s
)
SELECT customer_state, product_category, ROUND(revenue, 2) AS revenue, rnk
FROM ranked WHERE rnk <= 3
ORDER BY customer_state, rnk;

-- 7. Late delivery vs review score
SELECT is_late,
       COUNT(*) AS orders,
       ROUND(AVG(review_score), 2) AS avg_review,
       ROUND(AVG(delivery_days), 1) AS avg_delivery_days
FROM (SELECT DISTINCT order_id, is_late, review_score, delivery_days FROM fact_sales) o
GROUP BY is_late;

-- 8. Late-delivery % by state (worst 10)
SELECT customer_state,
       COUNT(*) AS orders,
       ROUND(100.0 * AVG(is_late), 2) AS late_pct
FROM (SELECT DISTINCT order_id, customer_state, is_late FROM fact_sales) o
GROUP BY customer_state
HAVING COUNT(*) > 100
ORDER BY late_pct DESC
LIMIT 10;

-- 9. Payment method mix
SELECT payment_type,
       COUNT(DISTINCT order_id) AS orders,
       ROUND(100.0 * COUNT(DISTINCT order_id) /
             (SELECT COUNT(DISTINCT order_id) FROM fact_sales), 2) AS pct
FROM fact_sales GROUP BY payment_type ORDER BY orders DESC;

-- 10. Revenue by RFM segment (joins the rfm table)
SELECT r.Segment,
       COUNT(DISTINCT f.customer_unique_id) AS customers,
       ROUND(SUM(f.revenue), 2) AS revenue,
       ROUND(100.0 * SUM(f.revenue) / SUM(SUM(f.revenue)) OVER (), 2) AS revenue_pct
FROM fact_sales f
JOIN rfm r ON r.customer_unique_id = f.customer_unique_id
GROUP BY r.Segment
ORDER BY revenue DESC;

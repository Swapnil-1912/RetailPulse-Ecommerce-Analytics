"""
Step 4: Load cleaned CSVs into a SQLite database (no server needed).
For PostgreSQL/MySQL, use SQLAlchemy's create_engine(...) instead of sqlite3.
Run:  python notebooks/04_load_to_sql.py
"""
import sqlite3
import pandas as pd

conn = sqlite3.connect("data/ecommerce.db")
for table in ["fact_sales", "dim_customers", "dim_products", "dim_date", "rfm"]:
    pd.read_csv(f"data/cleaned/{table}.csv").to_sql(table, conn, if_exists="replace", index=False)
    print("loaded", table)
conn.close()

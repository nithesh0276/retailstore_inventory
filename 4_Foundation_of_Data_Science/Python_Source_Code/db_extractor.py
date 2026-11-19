import sqlite3
import os
import pandas as pd

"""
Database Extractor Module: Pulls operational tables into Pandas DataFrames.
Course: 25ITC31 Foundations of Data Science (Unit 2: Python Foundations & Data Processing)
"""

def get_database_path():
    candidates = [
        os.path.join(os.path.dirname(__file__), "..", "retail_store.db"),
        os.path.join(os.path.dirname(__file__), "..", "..", "2_Database_Management_System", "retail_store.db"),
        os.path.join(os.path.dirname(__file__), "..", "..", "retail_store.db"),
        r"d:\nithe\retail store inventory\Retail_Store_Inventory_and_Sales_Analysis_System\2_Database_Management_System\retail_store.db"
    ]
    for p in candidates:
        if os.path.exists(p):
            return os.path.abspath(p)
    return "retail_store.db"

def extract_raw_datasets():
    db_path = get_database_path()
    print(f"[EXTRACTOR] Connecting to database: {db_path}")
    conn = sqlite3.connect(db_path)

    # 1. Products with Category & Inventory
    products_query = """
    SELECT 
        p.product_id, p.product_name, p.category_id, c.category_name,
        p.unit_price, p.cost_price, p.reorder_level,
        COALESCE(i.available_stock, 0) AS available_stock,
        COALESCE(i.last_updated, p.created_at) AS last_stock_update
    FROM products p
    JOIN categories c ON p.category_id = c.category_id
    LEFT JOIN inventory i ON p.product_id = i.product_id;
    """
    df_products = pd.read_sql_query(products_query, conn)

    # 2. Complete Transaction Details with Customer attribution
    sales_query = """
    SELECT 
        st.transaction_id,
        st.transaction_date,
        st.customer_id,
        cust.customer_name,
        st.payment_mode,
        st.cashier_name,
        sd.detail_id,
        sd.product_id,
        p.product_name,
        c.category_name,
        sd.quantity_sold,
        sd.unit_price,
        sd.subtotal,
        p.cost_price
    FROM sales_transactions st
    JOIN customers cust ON st.customer_id = cust.customer_id
    JOIN sales_details sd ON st.transaction_id = sd.transaction_id
    JOIN products p ON sd.product_id = p.product_id
    JOIN categories c ON p.category_id = c.category_id;
    """
    df_sales = pd.read_sql_query(sales_query, conn)

    # 3. Categories Summary
    df_categories = pd.read_sql_query("SELECT * FROM categories;", conn)

    # 4. Stock Updates Audit Log
    df_audits = pd.read_sql_query("SELECT * FROM stock_updates;", conn)

    conn.close()
    print(f"[EXTRACTOR] Extracted {len(df_products)} products, {len(df_sales)} sales items, {len(df_categories)} categories, {len(df_audits)} audit logs.")
    return df_products, df_sales, df_categories, df_audits

if __name__ == "__main__":
    p, s, c, a = extract_raw_datasets()
    print(p.head())

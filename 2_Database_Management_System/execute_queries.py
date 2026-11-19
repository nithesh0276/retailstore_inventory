import sqlite3
import os

BASE_DIR = r"d:\nithe\retail store inventory\Retail_Store_Inventory_and_Sales_Analysis_System\2_Database_Management_System"
DB_PATH = os.path.join(BASE_DIR, "retail_store.db")
OUTPUT_FILE = os.path.join(BASE_DIR, "Output", "query_execution_output.txt")
QUERIES_DIR = os.path.join(BASE_DIR, "Queries")

def run_all_queries():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    out_lines = []
    out_lines.append("=" * 90)
    out_lines.append("DATABASE QUERY EXECUTION REPORT: RETAIL STORE SYSTEM")
    out_lines.append("Academic Regulation: VCET B.Tech IT (R2025) | Course: 25ITT31 DBMS")
    out_lines.append("=" * 90)

    # 1. Basic Queries
    out_lines.append("\n" + "#" * 80)
    out_lines.append("SECTION 1: BASIC QUERIES (Selection, Projection, Sorting, Filtering)")
    out_lines.append("#" * 80)
    
    q1 = "SELECT product_id, product_name, unit_price, cost_price, reorder_level FROM products LIMIT 5;"
    out_lines.append(f"\n[QUERY 1.1] Sample Products Catalog:\nSQL: {q1}\n")
    cursor.execute(q1)
    rows = cursor.fetchall()
    out_lines.append(f"{'ID':<4} | {'PRODUCT NAME':<35} | {'PRICE ($)':<10} | {'COST ($)':<10} | {'REORDER':<8}")
    out_lines.append("-" * 75)
    for r in rows:
        out_lines.append(f"{r[0]:<4} | {r[1]:<35} | {r[2]:<10.2f} | {r[3]:<10.2f} | {r[4]:<8}")

    # 2. Joins & Aggregations
    out_lines.append("\n" + "#" * 80)
    out_lines.append("SECTION 2: JOINS & AGGREGATE FUNCTIONS")
    out_lines.append("#" * 80)

    q2 = """
    SELECT 
        p.product_id, p.product_name, c.category_name, p.unit_price, i.available_stock,
        ROUND(p.unit_price * i.available_stock, 2) AS stock_value
    FROM products p
    JOIN categories c ON p.category_id = c.category_id
    JOIN inventory i ON p.product_id = i.product_id
    LIMIT 6;
    """
    out_lines.append(f"\n[QUERY 2.1] Inventory Valuation (3-Table Join):\nSQL: {q2.strip()}\n")
    cursor.execute(q2)
    rows = cursor.fetchall()
    out_lines.append(f"{'ID':<4} | {'PRODUCT NAME':<32} | {'CATEGORY':<20} | {'PRICE':<8} | {'STOCK':<6} | {'VALUATION ($)':<12}")
    out_lines.append("-" * 92)
    for r in rows:
        out_lines.append(f"{r[0]:<4} | {r[1]:<32} | {r[2]:<20} | {r[3]:<8.2f} | {r[4]:<6} | {r[5]:<12.2f}")

    q3 = """
    SELECT 
        c.category_name,
        COUNT(DISTINCT p.product_id) AS items_count,
        COALESCE(SUM(sd.quantity_sold), 0) AS total_units_sold,
        ROUND(COALESCE(SUM(sd.subtotal), 0.0), 2) AS category_revenue
    FROM categories c
    JOIN products p ON c.category_id = p.category_id
    LEFT JOIN sales_details sd ON p.product_id = sd.product_id
    GROUP BY c.category_id, c.category_name
    ORDER BY category_revenue DESC;
    """
    out_lines.append(f"\n[QUERY 2.2] Category-wise Revenue Aggregation (GROUP BY):\nSQL: {q3.strip()}\n")
    cursor.execute(q3)
    rows = cursor.fetchall()
    out_lines.append(f"{'CATEGORY':<25} | {'ITEMS':<6} | {'UNITS SOLD':<11} | {'REVENUE ($)':<12}")
    out_lines.append("-" * 62)
    for r in rows:
        out_lines.append(f"{r[0]:<25} | {r[1]:<6} | {r[2]:<11} | {r[3]:<12.2f}")

    # 3. Views
    out_lines.append("\n" + "#" * 80)
    out_lines.append("SECTION 3: ANALYTICAL DATABASE VIEWS")
    out_lines.append("#" * 80)

    q4 = "SELECT sale_date, total_orders, total_revenue, average_order_value, total_units_sold FROM v_daily_sales_summary ORDER BY sale_date DESC;"
    out_lines.append(f"\n[VIEW 1] Daily Sales Summary (v_daily_sales_summary):\nSQL: {q4}\n")
    cursor.execute(q4)
    rows = cursor.fetchall()
    out_lines.append(f"{'SALE DATE':<12} | {'ORDERS':<8} | {'REVENUE ($)':<12} | {'AOV ($)':<10} | {'UNITS SOLD':<10}")
    out_lines.append("-" * 62)
    for r in rows:
        out_lines.append(f"{r[0]:<12} | {r[1]:<8} | {r[2]:<12.2f} | {r[3]:<10.2f} | {r[4]:<10}")

    q5 = "SELECT product_id, product_name, category_name, available_stock, reorder_level, alert_status FROM v_low_stock_alerts ORDER BY available_stock ASC;"
    out_lines.append(f"\n[VIEW 2] Low Stock Alerts (v_low_stock_alerts):\nSQL: {q5}\n")
    cursor.execute(q5)
    rows = cursor.fetchall()
    out_lines.append(f"{'ID':<4} | {'PRODUCT NAME':<35} | {'CATEGORY':<20} | {'STOCK':<6} | {'REORDER':<8} | {'STATUS':<12}")
    out_lines.append("-" * 94)
    for r in rows:
        out_lines.append(f"{r[0]:<4} | {r[1]:<35} | {r[2]:<20} | {r[3]:<6} | {r[4]:<8} | {r[5]:<12}")

    # 4. Top Fast Selling
    out_lines.append("\n" + "#" * 80)
    out_lines.append("SECTION 4: BUSINESS INTELLIGENCE (Fast-Selling Products)")
    out_lines.append("#" * 80)

    q6 = """
    SELECT 
        p.product_id, p.product_name, c.category_name,
        SUM(sd.quantity_sold) AS units_sold,
        ROUND(SUM(sd.subtotal), 2) AS total_revenue,
        i.available_stock
    FROM products p
    JOIN categories c ON p.category_id = c.category_id
    JOIN sales_details sd ON p.product_id = sd.product_id
    JOIN inventory i ON p.product_id = i.product_id
    GROUP BY p.product_id
    ORDER BY units_sold DESC
    LIMIT 5;
    """
    out_lines.append(f"\n[REPORT] Top 5 Fast-Selling Products:\nSQL: {q6.strip()}\n")
    cursor.execute(q6)
    rows = cursor.fetchall()
    out_lines.append(f"{'ID':<4} | {'PRODUCT NAME':<32} | {'CATEGORY':<20} | {'UNITS':<6} | {'REVENUE ($)':<12} | {'ON-HAND':<8}")
    out_lines.append("-" * 92)
    for r in rows:
        out_lines.append(f"{r[0]:<4} | {r[1]:<32} | {r[2]:<20} | {r[3]:<6} | {r[4]:<12.2f} | {r[5]:<8}")

    conn.close()

    full_output = "\n".join(out_lines)
    print(full_output)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(full_output)
    print(f"\n[SUCCESS] Query execution output saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    run_all_queries()

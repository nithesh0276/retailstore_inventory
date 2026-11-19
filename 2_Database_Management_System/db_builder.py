import sqlite3
import os
import sys

BASE_DIR = r"d:\nithe\retail store inventory\Retail_Store_Inventory_and_Sales_Analysis_System"
DB_DIR = os.path.join(BASE_DIR, "2_Database_Management_System")
SQL_FILE = os.path.join(DB_DIR, "SQL_Scripts", "04_master_setup.sql")
DB_PATH = os.path.join(DB_DIR, "retail_store.db")
OUTPUT_FILE = os.path.join(DB_DIR, "Output", "db_setup_output.txt")

def init_database():
    print("=" * 70)
    print("RETAIL STORE INVENTORY AND SALES ANALYSIS SYSTEM - DATABASE SETUP")
    print("Academic Regulation: VCET B.Tech IT (R2025) | Course: 25ITT31 DBMS")
    print("=" * 70)

    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
            print(f"[INFO] Removed existing database: {DB_PATH}")
        except Exception as e:
            print(f"[WARN] Could not remove existing DB: {e}")

    with open(SQL_FILE, 'r', encoding='utf-8') as f:
        sql_script = f.read()

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    try:
        cursor.executescript(sql_script)
        conn.commit()
        print(f"[SUCCESS] Executed master setup script: {SQL_FILE}")
        print(f"[SUCCESS] Database created successfully at: {DB_PATH}")
    except Exception as e:
        print(f"[ERROR] Database initialization failed: {e}")
        conn.close()
        sys.exit(1)

    # Verification queries
    verification_log = []
    verification_log.append("=" * 80)
    verification_log.append("DATABASE INITIALIZATION & VERIFICATION SUMMARY")
    verification_log.append("=" * 80)

    tables = ["categories", "products", "customers", "inventory", "sales_transactions", "sales_details", "stock_updates"]
    verification_log.append(f"\n{'TABLE NAME':<25} | {'RECORD COUNT':<15} | {'STATUS':<15}")
    verification_log.append("-" * 60)

    for tbl in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {tbl};")
        count = cursor.fetchone()[0]
        verification_log.append(f"{tbl:<25} | {count:<15} | {'OK (Active)':<15}")

    # Views verification
    views = ["v_daily_sales_summary", "v_low_stock_alerts", "v_product_sales_performance", "v_category_revenue"]
    verification_log.append(f"\n{'DATABASE VIEW':<30} | {'ROW COUNT':<15} | {'STATUS':<15}")
    verification_log.append("-" * 65)
    for vw in views:
        cursor.execute(f"SELECT COUNT(*) FROM {vw};")
        count = cursor.fetchone()[0]
        verification_log.append(f"{vw:<30} | {count:<15} | {'OK (Active)':<15}")

    # Triggers verification
    cursor.execute("SELECT name, tbl_name FROM sqlite_master WHERE type = 'trigger';")
    trg_rows = cursor.fetchall()
    verification_log.append(f"\n{'TRIGGER NAME':<30} | {'ATTACHED TABLE':<20} | {'STATUS':<15}")
    verification_log.append("-" * 70)
    for trg, tbl in trg_rows:
        verification_log.append(f"{trg:<30} | {tbl:<20} | {'ARMED':<15}")

    conn.close()

    summary_text = "\n".join(verification_log)
    print(summary_text)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(summary_text)
    print(f"\n[INFO] Verification report saved to: {OUTPUT_FILE}")

    # Also sync a copy to Java and Python folders and project root
    sync_targets = [
        os.path.join(BASE_DIR, "retail_store.db"),
        os.path.join(BASE_DIR, "3_Java_Programming", "retail_store.db"),
        os.path.join(BASE_DIR, "4_Foundation_of_Data_Science", "retail_store.db")
    ]
    for target in sync_targets:
        import shutil
        shutil.copyfile(DB_PATH, target)
        print(f"[SYNC] Mirrored database to: {target}")

if __name__ == "__main__":
    init_database()

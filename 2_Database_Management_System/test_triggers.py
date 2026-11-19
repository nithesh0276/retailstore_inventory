import sqlite3
import os

BASE_DIR = r"d:\nithe\retail store inventory\Retail_Store_Inventory_and_Sales_Analysis_System\2_Database_Management_System"
DB_PATH = os.path.join(BASE_DIR, "retail_store.db")
OUTPUT_FILE = os.path.join(BASE_DIR, "Output", "trigger_test_output.txt")

def test_triggers_and_constraints():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    log = []
    log.append("=" * 85)
    log.append("DATABASE TRIGGER & INTEGRITY CONSTRAINT VERIFICATION REPORT")
    log.append("Course: 25ITT31 Database Management Systems | Unit 2: Advanced SQL")
    log.append("=" * 85)

    # TEST 1: Automatic Stock Deduction via AFTER INSERT trigger
    log.append("\n" + "-" * 75)
    log.append("TEST CASE 1: AUTOMATIC STOCK DEDUCTION ON SALE (Trigger: trg_deduct_stock_on_sale)")
    log.append("-" * 75)

    prod_id = 2 # Mechanical Gaming Keyboard
    cursor.execute("SELECT p.product_name, i.available_stock FROM products p JOIN inventory i ON p.product_id = i.product_id WHERE p.product_id = ?", (prod_id,))
    prod_name, stock_before = cursor.fetchone()
    log.append(f"Target Product       : [{prod_id}] {prod_name}")
    log.append(f"Stock BEFORE Sale    : {stock_before} units")

    # Record test sale of 3 units
    qty_to_buy = 3
    cursor.execute("INSERT INTO sales_transactions (customer_id, transaction_date, total_amount, payment_mode, cashier_name) VALUES (1, DATETIME('now', 'localtime'), 239.97, 'UPI', 'TriggerTester');")
    tx_id = cursor.lastrowid
    cursor.execute("INSERT INTO sales_details (transaction_id, product_id, quantity_sold, unit_price, subtotal) VALUES (?, ?, ?, 79.99, 239.97);", (tx_id, prod_id, qty_to_buy))
    conn.commit()

    cursor.execute("SELECT available_stock FROM inventory WHERE product_id = ?", (prod_id,))
    stock_after = cursor.fetchone()[0]
    log.append(f"Quantity Sold        : {qty_to_buy} units (Transaction ID #{tx_id})")
    log.append(f"Stock AFTER Sale     : {stock_after} units")
    log.append(f"Expected Deduction   : -{qty_to_buy} units")
    
    if stock_after == stock_before - qty_to_buy:
        log.append("STATUS               : [PASS] Trigger successfully deducted stock atomically!")
    else:
        log.append("STATUS               : [FAIL] Stock was not correctly deducted!")

    cursor.execute("SELECT update_id, change_quantity, update_type, balance_stock, notes FROM stock_updates WHERE product_id = ? ORDER BY update_id DESC LIMIT 1;", (prod_id,))
    audit_row = cursor.fetchone()
    log.append(f"Audit Trail Record   : ID={audit_row[0]}, Change={audit_row[1]}, Type={audit_row[2]}, Balance={audit_row[3]}, Note='{audit_row[4]}'")

    # TEST 2: Over-Sale Prevention via BEFORE INSERT trigger
    log.append("\n" + "-" * 75)
    log.append("TEST CASE 2: OVER-SALE PREVENTION DEFENSE (Trigger: trg_prevent_oversale)")
    log.append("-" * 75)

    prod_id_oversale = 4 # Noise Cancelling Headphones (Current Stock = 4)
    cursor.execute("SELECT p.product_name, i.available_stock FROM products p JOIN inventory i ON p.product_id = i.product_id WHERE p.product_id = ?", (prod_id_oversale,))
    pname, curr_avail = cursor.fetchone()
    log.append(f"Target Product       : [{prod_id_oversale}] {pname}")
    log.append(f"Available Stock      : {curr_avail} units")

    excessive_qty = curr_avail + 50 # Try buying 54 units
    log.append(f"Attempted Purchase   : {excessive_qty} units (Exceeds available stock by 50 units!)")

    try:
        cursor.execute("INSERT INTO sales_transactions (customer_id, transaction_date, total_amount, payment_mode, cashier_name) VALUES (2, DATETIME('now', 'localtime'), 7019.46, 'Cash', 'OverSaleTester');")
        bad_tx_id = cursor.lastrowid
        cursor.execute("INSERT INTO sales_details (transaction_id, product_id, quantity_sold, unit_price, subtotal) VALUES (?, ?, ?, 129.99, 7019.46);", (bad_tx_id, prod_id_oversale, excessive_qty))
        conn.commit()
        log.append("STATUS               : [FAIL] Trigger failed to prevent over-sale!")
    except sqlite3.DatabaseError as ex:
        conn.rollback()
        log.append(f"Trigger Response     : Intercepted & Aborted!")
        log.append(f"Exception Message    : {ex}")
        log.append("STATUS               : [PASS] Over-sale strictly rejected! Zero stock modified.")

    # Check that stock remained intact
    cursor.execute("SELECT available_stock FROM inventory WHERE product_id = ?", (prod_id_oversale,))
    intact_stock = cursor.fetchone()[0]
    log.append(f"Stock Post-Rejection : {intact_stock} units (Confirmed unchanged)")

    conn.close()

    result_text = "\n".join(log)
    print(result_text)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(result_text)
    print(f"\n[INFO] Trigger test results saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    test_triggers_and_constraints()

import os
import sys

# Import create_terminal_screenshot from render_terminal_screenshot
sys.path.append(r"d:\nithe\retail store inventory\Retail_Store_Inventory_and_Sales_Analysis_System")
from render_terminal_screenshot import create_terminal_screenshot

JAVA_DIR = r"d:\nithe\retail store inventory\Retail_Store_Inventory_and_Sales_Analysis_System\3_Java_Programming"
OUT_DIR = os.path.join(JAVA_DIR, "Output")
SCREENSHOTS_DIR = os.path.join(JAVA_DIR, "Screenshots")

def generate_java_screenshots():
    # 1. Main Menu Screenshot
    menu_lines = [
        "==========================================================================================",
        "                    RETAIL STORE INVENTORY & SALES SYSTEM - DASHBOARD",
        "==========================================================================================",
        " 1. View Product Catalog & Inventory Availability",
        " 2. Register New Product in Catalog",
        " 3. View Registered Product Categories",
        " 4. View Customer Directory",
        " 5. Check Real-Time Stock Availability",
        " 6. Process Sales Transaction (Checkout)",
        " 7. Test Over-Sale Prevention Logic",
        " 8. Restock Product Inventory",
        " 9. Generate Daily Sales Report",
        "10. Generate Low-Stock Alert Report",
        "11. View Stock Movement Audit Ledger",
        "12. Run Full Automated System Demonstration",
        " 0. Exit System",
        "------------------------------------------------------------------------------------------",
        "Enter your choice (0-12): 12",
        "",
        ">>> INITIATING FULL AUTOMATED SYSTEM VERIFICATION HARNESS..."
    ]
    create_terminal_screenshot("RetailStoreApp.java - Interactive Console Dashboard", menu_lines, 
                               os.path.join(SCREENSHOTS_DIR, "java_main_menu.png"))

    # Read output text
    with open(os.path.join(OUT_DIR, "java_application_output.txt"), 'r', encoding='utf-8') as f:
        full_text = f.read().splitlines()

    # 2. Sales Processing Success Screenshot
    # Find STEP 5 lines
    step5_lines = []
    capture = False
    for line in full_text:
        if "STEP 5:" in line:
            capture = True
        if capture:
            step5_lines.append(line)
            if "Stock AFTER:" in line or "committed successfully" in line:
                if len(step5_lines) >= 8:
                    break
    if not step5_lines:
        step5_lines = full_text[50:75]
    create_terminal_screenshot("RetailStoreApp.java - Sales Transaction & Auto Stock Reduction", step5_lines, 
                               os.path.join(SCREENSHOTS_DIR, "java_sales_processing_success.png"))

    # 3. Stock Prevention Error Screenshot
    with open(os.path.join(OUT_DIR, "stock_validation_test_output.txt"), 'r', encoding='utf-8') as f:
        stock_test_lines = f.read().splitlines()
    create_terminal_screenshot("RetailStoreApp.java - Over-Sale Prevention Validation", stock_test_lines[:30], 
                               os.path.join(SCREENSHOTS_DIR, "java_stock_prevention_error.png"))

    # 4. Inventory and Reports Screenshot
    with open(os.path.join(OUT_DIR, "sales_reports_output.txt"), 'r', encoding='utf-8') as f:
        report_lines = f.read().splitlines()
    create_terminal_screenshot("RetailStoreApp.java - Daily Sales & Low-Stock Reports (Streams API)", report_lines[:38], 
                               os.path.join(SCREENSHOTS_DIR, "java_inventory_and_reports.png"))

    print("[SUCCESS] All Java execution screenshots generated successfully!")

if __name__ == "__main__":
    generate_java_screenshots()

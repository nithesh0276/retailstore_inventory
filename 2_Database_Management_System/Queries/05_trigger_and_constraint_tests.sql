-- ==============================================================================
-- 05_trigger_and_constraint_tests.sql: Trigger Validation & Constraint Checks
-- Retail Store Inventory and Sales Analysis System
-- Course: 25ITT31 - Database Management Systems (Unit 2: SQL Triggers & Integrity)
-- ==============================================================================

PRAGMA foreign_keys = ON;

-- ------------------------------------------------------------------------------
-- TEST 1: Automatic Stock Deduction & Audit Logging Verification
-- Product ID 2: Initial available_stock = 38 - (1 sold in tx 101) - (1 in tx 108) = 36
-- Let's inspect current stock before test transaction:
-- ------------------------------------------------------------------------------
SELECT '=== BEFORE TEST SALE ===' AS test_status;
SELECT product_id, available_stock, last_updated 
FROM inventory 
WHERE product_id = 2;

-- Process a new test sale of 2 units of Product ID 2
INSERT INTO sales_transactions (customer_id, transaction_date, total_amount, payment_mode, cashier_name)
VALUES (1, DATETIME('now', 'localtime'), 159.98, 'Credit Card', 'Automated Test Runner');

-- Insert line item (Trigger trg_deduct_stock_on_sale fires here)
INSERT INTO sales_details (transaction_id, product_id, quantity_sold, unit_price, subtotal)
VALUES ((SELECT MAX(transaction_id) FROM sales_transactions), 2, 2, 79.99, 159.98);

SELECT '=== AFTER TEST SALE (STOCK MUST DECREASE BY 2) ===' AS test_status;
SELECT product_id, available_stock, last_updated 
FROM inventory 
WHERE product_id = 2;

SELECT '=== AUDIT LEDGER ENTRY CREATED BY TRIGGER ===' AS test_status;
SELECT update_id, product_id, change_quantity, update_type, balance_stock, notes
FROM stock_updates 
WHERE product_id = 2 
ORDER BY update_id DESC 
LIMIT 1;

-- ------------------------------------------------------------------------------
-- TEST 2: Over-Sale Prevention Trigger Verification
-- Product ID 4 currently has available_stock = 4
-- Attempting to purchase 100 units must fail and raise an ABORT exception!
-- ------------------------------------------------------------------------------
SELECT '=== ATTEMPTING OVER-SALE SALE (EXPECTING TRIGGER TO ABORT) ===' AS test_status;

-- The following INSERT will be aborted by trigger trg_prevent_oversale:
-- INSERT INTO sales_details (transaction_id, product_id, quantity_sold, unit_price, subtotal)
-- VALUES (101, 4, 100, 129.99, 12999.00);
-- Result: "INSUFFICIENT_STOCK_ERROR: Requested quantity exceeds available inventory stock!"

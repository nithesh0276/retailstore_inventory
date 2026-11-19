-- ==============================================================================
-- 02_triggers_and_views.sql: Database Triggers, Constraints & Analytical Views
-- Retail Store Inventory and Sales Analysis System
-- Course: 25ITT31 - Database Management Systems (Unit 2: Advanced SQL & Views)
-- ==============================================================================

PRAGMA foreign_keys = ON;

-- Drop existing triggers and views to allow clean re-execution
DROP TRIGGER IF EXISTS trg_prevent_oversale;
DROP TRIGGER IF EXISTS trg_deduct_stock_on_sale;
DROP TRIGGER IF EXISTS trg_audit_restock;

DROP VIEW IF EXISTS v_daily_sales_summary;
DROP VIEW IF EXISTS v_low_stock_alerts;
DROP VIEW IF EXISTS v_product_sales_performance;
DROP VIEW IF EXISTS v_category_revenue;

-- ==============================================================================
-- DATABASE TRIGGERS
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- Trigger 1: trg_prevent_oversale
-- Concept: Integrity constraint defense. Rejects sales exceeding on-hand stock.
-- ------------------------------------------------------------------------------
CREATE TRIGGER trg_prevent_oversale
BEFORE INSERT ON sales_details
FOR EACH ROW
WHEN NEW.quantity_sold > (SELECT available_stock FROM inventory WHERE product_id = NEW.product_id)
BEGIN
    SELECT RAISE(ABORT, 'INSUFFICIENT_STOCK_ERROR: Requested quantity exceeds available inventory stock!');
END;

-- ------------------------------------------------------------------------------
-- Trigger 2: trg_deduct_stock_on_sale
-- Concept: Automated stock quantity update and audit trail logging upon sale.
-- ------------------------------------------------------------------------------
CREATE TRIGGER trg_deduct_stock_on_sale
AFTER INSERT ON sales_details
FOR EACH ROW
BEGIN
    -- 1. Automatically decrement available stock in inventory
    UPDATE inventory 
    SET available_stock = available_stock - NEW.quantity_sold,
        last_updated = DATETIME('now', 'localtime')
    WHERE product_id = NEW.product_id;

    -- 2. Insert audit entry into stock_updates
    INSERT INTO stock_updates (product_id, change_quantity, update_type, balance_stock, notes)
    VALUES (
        NEW.product_id, 
        -NEW.quantity_sold, 
        'SALE', 
        (SELECT available_stock FROM inventory WHERE product_id = NEW.product_id),
        'Auto stock deduction for Sales Transaction #' || NEW.transaction_id || ' (Qty: ' || NEW.quantity_sold || ')'
    );
END;

-- ------------------------------------------------------------------------------
-- Trigger 3: trg_audit_restock
-- Concept: Logs stock replenishment events to the immutable audit ledger.
-- ------------------------------------------------------------------------------
CREATE TRIGGER trg_audit_restock
AFTER UPDATE OF available_stock ON inventory
FOR EACH ROW
WHEN NEW.available_stock > OLD.available_stock
BEGIN
    INSERT INTO stock_updates (product_id, change_quantity, update_type, balance_stock, notes)
    VALUES (
        NEW.product_id,
        NEW.available_stock - OLD.available_stock,
        'RESTOCK',
        NEW.available_stock,
        'Stock replenishment: Added ' || (NEW.available_stock - OLD.available_stock) || ' units'
    );
END;

-- ==============================================================================
-- ANALYTICAL DATABASE VIEWS
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- View 1: v_daily_sales_summary
-- Aggregates orders, gross revenue, and units sold per calendar date.
-- ------------------------------------------------------------------------------
CREATE VIEW v_daily_sales_summary AS
SELECT 
    SUBSTR(st.transaction_date, 1, 10) AS sale_date,
    COUNT(DISTINCT st.transaction_id) AS total_orders,
    ROUND(SUM(st.total_amount), 2) AS total_revenue,
    ROUND(AVG(st.total_amount), 2) AS average_order_value,
    SUM(sd.quantity_sold) AS total_units_sold
FROM sales_transactions st
JOIN sales_details sd ON st.transaction_id = sd.transaction_id
GROUP BY SUBSTR(st.transaction_date, 1, 10);

-- ------------------------------------------------------------------------------
-- View 2: v_low_stock_alerts
-- Proactively flags products where stock has fallen below the reorder threshold.
-- ------------------------------------------------------------------------------
CREATE VIEW v_low_stock_alerts AS
SELECT 
    p.product_id,
    p.product_name,
    c.category_name,
    i.available_stock,
    p.reorder_level,
    (p.reorder_level - i.available_stock) AS reorder_urgency,
    CASE 
        WHEN i.available_stock = 0 THEN 'OUT_OF_STOCK'
        WHEN i.available_stock <= (p.reorder_level / 2) THEN 'CRITICAL'
        ELSE 'LOW_STOCK'
    END AS alert_status
FROM products p
JOIN categories c ON p.category_id = c.category_id
JOIN inventory i ON p.product_id = i.product_id
WHERE i.available_stock <= p.reorder_level;

-- ------------------------------------------------------------------------------
-- View 3: v_product_sales_performance
-- Combines catalog, sales, margins, and inventory positions per product.
-- ------------------------------------------------------------------------------
CREATE VIEW v_product_sales_performance AS
SELECT 
    p.product_id,
    p.product_name,
    c.category_name,
    p.unit_price,
    p.cost_price,
    COALESCE(SUM(sd.quantity_sold), 0) AS total_units_sold,
    ROUND(COALESCE(SUM(sd.subtotal), 0.0), 2) AS total_revenue,
    ROUND(COALESCE(SUM(sd.quantity_sold * (sd.unit_price - p.cost_price)), 0.0), 2) AS gross_profit,
    i.available_stock,
    p.reorder_level
FROM products p
JOIN categories c ON p.category_id = c.category_id
JOIN inventory i ON p.product_id = i.product_id
LEFT JOIN sales_details sd ON p.product_id = sd.product_id
GROUP BY p.product_id;

-- ------------------------------------------------------------------------------
-- View 4: v_category_revenue
-- Summarizes sales turnover and product count grouped by category.
-- ------------------------------------------------------------------------------
CREATE VIEW v_category_revenue AS
SELECT 
    c.category_id,
    c.category_name,
    COUNT(DISTINCT p.product_id) AS product_count,
    COALESCE(SUM(sd.quantity_sold), 0) AS total_units_sold,
    ROUND(COALESCE(SUM(sd.subtotal), 0.0), 2) AS total_revenue
FROM categories c
LEFT JOIN products p ON c.category_id = p.category_id
LEFT JOIN sales_details sd ON p.product_id = sd.product_id
GROUP BY c.category_id;

-- ==============================================================================
-- 04_business_reports.sql: Advanced Business Intelligence and Reporting Queries
-- Retail Store Inventory and Sales Analysis System
-- Course: 25ITT31 - Database Management Systems (Unit 2: Analytical SQL)
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- REPORT 1: Fast-Selling Products (Top 5 by Sales Volume & Revenue)
-- ------------------------------------------------------------------------------
SELECT 
    p.product_id,
    p.product_name,
    c.category_name,
    SUM(sd.quantity_sold) AS units_sold,
    ROUND(SUM(sd.subtotal), 2) AS total_sales_volume,
    i.available_stock AS remaining_stock
FROM products p
JOIN categories c ON p.category_id = c.category_id
JOIN sales_details sd ON p.product_id = sd.product_id
JOIN inventory i ON p.product_id = i.product_id
GROUP BY p.product_id, p.product_name, c.category_name, i.available_stock
ORDER BY units_sold DESC, total_sales_volume DESC
LIMIT 5;

-- ------------------------------------------------------------------------------
-- REPORT 2: Critical Inventory Valuation and Restock Reorder Requirements
-- ------------------------------------------------------------------------------
SELECT 
    p.product_id,
    p.product_name,
    c.category_name,
    i.available_stock,
    p.reorder_level,
    (p.reorder_level * 2 - i.available_stock) AS recommended_reorder_qty,
    ROUND((p.reorder_level * 2 - i.available_stock) * p.cost_price, 2) AS estimated_restock_cost
FROM products p
JOIN categories c ON p.category_id = c.category_id
JOIN inventory i ON p.product_id = i.product_id
WHERE i.available_stock <= p.reorder_level
ORDER BY (p.reorder_level - i.available_stock) DESC;

-- ------------------------------------------------------------------------------
-- REPORT 3: Profit Margin and Gross Margin Return on Inventory (GMROI)
-- ------------------------------------------------------------------------------
SELECT 
    p.product_id,
    p.product_name,
    p.unit_price,
    p.cost_price,
    ROUND((p.unit_price - p.cost_price), 2) AS profit_per_unit,
    ROUND(((p.unit_price - p.cost_price) / p.unit_price) * 100, 2) AS profit_margin_pct,
    COALESCE(SUM(sd.quantity_sold), 0) AS total_sold,
    ROUND(COALESCE(SUM(sd.quantity_sold * (sd.unit_price - p.cost_price)), 0), 2) AS total_gross_profit
FROM products p
LEFT JOIN sales_details sd ON p.product_id = sd.product_id
GROUP BY p.product_id
ORDER BY total_gross_profit DESC;

-- ------------------------------------------------------------------------------
-- REPORT 4: Audit Ledger of Stock Movements for Product ID 1 (Traceability)
-- ------------------------------------------------------------------------------
SELECT 
    su.update_id,
    su.product_id,
    p.product_name,
    su.change_quantity,
    su.update_type,
    su.balance_stock,
    su.update_timestamp,
    su.notes
FROM stock_updates su
JOIN products p ON su.product_id = p.product_id
WHERE su.product_id = 1
ORDER BY su.update_id ASC;

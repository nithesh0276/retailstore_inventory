-- ==============================================================================
-- 03_subqueries_and_views.sql: Nested Subqueries, Correlated Subqueries & Views
-- Retail Store Inventory and Sales Analysis System
-- Course: 25ITT31 - Database Management Systems (Unit 2: Subqueries & Views)
-- ==============================================================================

-- 1. Nested Subquery: Find products whose price is strictly above average catalog price
SELECT 
    product_id,
    product_name,
    unit_price,
    ROUND((SELECT AVG(unit_price) FROM products), 2) AS average_catalog_price
FROM products
WHERE unit_price > (SELECT AVG(unit_price) FROM products)
ORDER BY unit_price DESC;

-- 2. Correlated Subquery: Customers who have made more purchases than the store average
SELECT 
    c.customer_id,
    c.customer_name,
    c.phone,
    (SELECT COUNT(*) FROM sales_transactions st WHERE st.customer_id = c.customer_id) AS purchase_count
FROM customers c
WHERE (SELECT COUNT(*) FROM sales_transactions st WHERE st.customer_id = c.customer_id) > 
      (SELECT AVG(cust_orders.total_orders) FROM (
          SELECT COUNT(*) AS total_orders FROM sales_transactions GROUP BY customer_id
      ) AS cust_orders)
ORDER BY purchase_count DESC;

-- 3. Querying Database View: Daily Sales Summary
SELECT 
    sale_date,
    total_orders,
    total_revenue,
    average_order_value,
    total_units_sold
FROM v_daily_sales_summary
ORDER BY sale_date DESC;

-- 4. Querying Database View: Low Stock Alerts
SELECT 
    product_id,
    product_name,
    category_name,
    available_stock,
    reorder_level,
    reorder_urgency,
    alert_status
FROM v_low_stock_alerts
ORDER BY available_stock ASC;

-- 5. Querying Database View: Product Sales Performance
SELECT 
    product_id,
    product_name,
    category_name,
    unit_price,
    total_units_sold,
    total_revenue,
    gross_profit,
    available_stock
FROM v_product_sales_performance
ORDER BY total_revenue DESC;

-- 6. Querying Database View: Category Revenue Breakdown
SELECT 
    category_id,
    category_name,
    product_count,
    total_units_sold,
    total_revenue
FROM v_category_revenue
ORDER BY total_revenue DESC;

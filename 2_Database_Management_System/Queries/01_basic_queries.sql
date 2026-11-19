-- ==============================================================================
-- 01_basic_queries.sql: Basic DQL Queries (Select, Filter, Sorting, Projections)
-- Retail Store Inventory and Sales Analysis System
-- Course: 25ITT31 - Database Management Systems (Unit 2: SQL Basics)
-- ==============================================================================

-- 1. Retrieve all registered product categories
SELECT category_id, category_name, description 
FROM categories 
ORDER BY category_id;

-- 2. Retrieve all products with pricing sorted by unit price descending
SELECT product_id, product_name, unit_price, cost_price, reorder_level 
FROM products 
ORDER BY unit_price DESC;

-- 3. Filter products priced between $10.00 and $50.00
SELECT product_id, product_name, unit_price 
FROM products 
WHERE unit_price BETWEEN 10.00 AND 50.00
ORDER BY unit_price ASC;

-- 4. Search products by keyword pattern (e.g. products containing 'Tea' or 'Coffee')
SELECT product_id, product_name, unit_price 
FROM products 
WHERE product_name LIKE '%Tea%' OR product_name LIKE '%Coffee%';

-- 5. Retrieve all registered customers sorted alphabetically by name
SELECT customer_id, customer_name, phone, email, address 
FROM customers 
ORDER BY customer_name ASC;

-- 6. Retrieve distinct payment modes used across all transactions
SELECT DISTINCT payment_mode 
FROM sales_transactions;

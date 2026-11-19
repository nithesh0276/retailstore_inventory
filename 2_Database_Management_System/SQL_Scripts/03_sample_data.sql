-- ==============================================================================
-- 03_sample_data.sql: Realistic Sample Data Seeding Script
-- Retail Store Inventory and Sales Analysis System
-- Course: 25ITT31 - Database Management Systems (VCET R2025)
-- Register No: 9, 39, 69, 99
-- ==============================================================================

PRAGMA foreign_keys = ON;

-- ------------------------------------------------------------------------------
-- 1. Insert Categories (5 Major Retail Departments)
-- ------------------------------------------------------------------------------
INSERT INTO categories (category_id, category_name, description) VALUES
(1, 'Electronics', 'Consumer electronics, accessories, smart devices, and peripherals'),
(2, 'Groceries & Staples', 'Daily grocery staples, rice, flour, pulses, cooking oils, and condiments'),
(3, 'Beverages & Snacks', 'Packaged juices, organic tea, roasted coffees, sodas, and cookies'),
(4, 'Personal Care', 'Hygiene essentials, skincare, haircare, sanitizers, and soaps'),
(5, 'Home & Kitchen', 'Cookware, cleaning agents, organizers, and tableware');

-- ------------------------------------------------------------------------------
-- 2. Insert Products (20 Realistic Items with Cost and Reorder Levels)
-- ------------------------------------------------------------------------------
INSERT INTO products (product_id, product_name, category_id, unit_price, cost_price, reorder_level) VALUES
-- Electronics
(1, 'Wireless Optical Mouse', 1, 24.99, 14.50, 15),
(2, 'Mechanical Gaming Keyboard', 1, 79.99, 45.00, 10),
(3, 'USB-C Fast Charging Cable', 1, 12.99, 5.20, 20),
(4, 'Noise Cancelling Headphones', 1, 129.99, 75.00, 8),
-- Groceries & Staples
(5, 'Basmati Rice Premium (5kg)', 2, 18.50, 13.00, 25),
(6, 'Organic Wheat Flour (10kg)', 2, 22.00, 16.50, 20),
(7, 'Extra Virgin Olive Oil (1L)', 2, 14.99, 9.80, 12),
(8, 'Pure Golden Honey (500g)', 2, 8.50, 5.00, 15),
-- Beverages & Snacks
(9, 'Arabica Dark Roast Coffee Beans (500g)', 3, 16.99, 10.50, 12),
(10, 'Organic Green Tea (100 Bags)', 3, 9.99, 5.50, 18),
(11, 'Almond Butter Crunch Granola (400g)', 3, 6.49, 3.80, 15),
(12, 'Natural Coconut Water (1L)', 3, 4.25, 2.50, 30),
-- Personal Care
(13, 'Botanical Moisturizing Shampoo (400ml)', 4, 11.50, 6.20, 15),
(14, 'Antibacterial Hand Wash (500ml)', 4, 5.99, 3.10, 25),
(15, 'Charcoal Whitening Toothpaste (150g)', 4, 4.50, 2.20, 20),
(16, 'Moisturizing Aloe Vera Lotion (250ml)', 4, 8.99, 4.50, 10),
-- Home & Kitchen
(17, 'Stainless Steel Thermal Flask (1L)', 5, 19.99, 11.00, 10),
(18, 'Non-Stick Ceramic Frying Pan (28cm)', 5, 34.99, 21.00, 8),
(19, 'Microfiber Cleaning Cloth Set (6pk)', 5, 7.99, 3.50, 20),
(20, 'Aromatherapy Soy Scented Candle', 5, 13.50, 6.80, 12);

-- ------------------------------------------------------------------------------
-- 3. Insert Customers (10 Registered Regular Shoppers)
-- ------------------------------------------------------------------------------
INSERT INTO customers (customer_id, customer_name, phone, email, address) VALUES
(1, 'Aarav Sharma', '9876543210', 'aarav.sharma@example.com', '12 Lake View Residency, Sector 4'),
(2, 'Diya Patel', '9812345678', 'diya.patel@example.com', '45 Blossom Meadows, Tech Corridor'),
(3, 'Rohan Verma', '9723456789', 'rohan.verma@example.com', '88 Emerald Park, North Ring Road'),
(4, 'Ananya Iyer', '9634567890', 'ananya.iyer@example.com', '23 Temple Street, Heritage Town'),
(5, 'Vikram Malhotra', '9545678901', 'vikram.m@example.com', '104 Sky Towers, Financial District'),
(6, 'Pooja Hegde', '9456789012', 'pooja.h@example.com', '17 Lotus Colony, West Extension'),
(7, 'Karthik Raja', '9367890123', 'karthik.raja@example.com', '52 Anna Nagar East, Metro Road'),
(8, 'Sneha Mukherjee', '9278901234', 'sneha.m@example.com', '79 Riverside Enclave, Block B'),
(9, 'Rahul Dravid', '9189012345', 'rahul.d@example.com', '11 Pavilion Way, Sports Complex'),
(10, 'Meera Nambiar', '9090123456', 'meera.n@example.com', '66 Green Valley, Hill View Phase 2');

-- ------------------------------------------------------------------------------
-- 4. Insert Initial Inventory Position (Stock levels before historical sales)
-- Note: Products 4, 18, and 12 will intentionally reflect critical low-stock
-- ------------------------------------------------------------------------------
INSERT INTO inventory (inventory_id, product_id, available_stock, last_updated) VALUES
(1, 1, 65, '2026-11-01 09:00:00'),
(2, 2, 38, '2026-11-01 09:00:00'),
(3, 3, 90, '2026-11-01 09:00:00'),
(4, 4, 5,  '2026-11-01 09:00:00'), -- Low stock (Reorder level = 8, Available = 5)
(5, 5, 75, '2026-11-01 09:00:00'),
(6, 6, 50, '2026-11-01 09:00:00'),
(7, 7, 40, '2026-11-01 09:00:00'),
(8, 8, 45, '2026-11-01 09:00:00'),
(9, 9, 35, '2026-11-01 09:00:00'),
(10, 10, 60, '2026-11-01 09:00:00'),
(11, 11, 40, '2026-11-01 09:00:00'),
(12, 12, 8,  '2026-11-01 09:00:00'), -- Critical low stock (Reorder = 30, Available = 8)
(13, 13, 50, '2026-11-01 09:00:00'),
(14, 14, 80, '2026-11-01 09:00:00'),
(15, 15, 65, '2026-11-01 09:00:00'),
(16, 16, 30, '2026-11-01 09:00:00'),
(17, 17, 28, '2026-11-01 09:00:00'),
(18, 18, 4,  '2026-11-01 09:00:00'), -- Critical low stock (Reorder = 8, Available = 4)
(19, 19, 55, '2026-11-01 09:00:00'),
(20, 20, 32, '2026-11-01 09:00:00');

-- Initial stock audit log
INSERT INTO stock_updates (product_id, change_quantity, update_type, balance_stock, update_timestamp, notes)
SELECT product_id, available_stock, 'INITIAL', available_stock, last_updated, 'Opening stock initialization'
FROM inventory;

-- ------------------------------------------------------------------------------
-- 5. Insert Historical Sales Transactions (Dates: Nov 10 to Nov 18, 2026)
-- Note: When inserting sales_details, the trigger trg_deduct_stock_on_sale
-- will automatically update inventory and log into stock_updates!
-- ------------------------------------------------------------------------------

-- Transaction 101: 2026-11-10
INSERT INTO sales_transactions (transaction_id, customer_id, transaction_date, total_amount, payment_mode, cashier_name)
VALUES (101, 1, '2026-11-10 10:15:00', 104.98, 'Credit Card', 'John Doe');
INSERT INTO sales_details (transaction_id, product_id, quantity_sold, unit_price, subtotal) VALUES
(101, 1, 1, 24.99, 24.99),
(101, 2, 1, 79.99, 79.99);

-- Transaction 102: 2026-11-11
INSERT INTO sales_transactions (transaction_id, customer_id, transaction_date, total_amount, payment_mode, cashier_name)
VALUES (102, 2, '2026-11-11 11:30:00', 55.49, 'UPI', 'Alice Smith');
INSERT INTO sales_details (transaction_id, product_id, quantity_sold, unit_price, subtotal) VALUES
(102, 5, 2, 18.50, 37.00),
(102, 8, 1, 8.50, 8.50),
(102, 10, 1, 9.99, 9.99);

-- Transaction 103: 2026-11-11
INSERT INTO sales_transactions (transaction_id, customer_id, transaction_date, total_amount, payment_mode, cashier_name)
VALUES (103, 3, '2026-11-11 15:45:00', 64.95, 'Cash', 'John Doe');
INSERT INTO sales_details (transaction_id, product_id, quantity_sold, unit_price, subtotal) VALUES
(103, 3, 5, 12.99, 64.95);

-- Transaction 104: 2026-11-12
INSERT INTO sales_transactions (transaction_id, customer_id, transaction_date, total_amount, payment_mode, cashier_name)
VALUES (104, 4, '2026-11-12 14:10:00', 50.98, 'Debit Card', 'Alice Smith');
INSERT INTO sales_details (transaction_id, product_id, quantity_sold, unit_price, subtotal) VALUES
(104, 7, 2, 14.99, 29.98),
(104, 9, 1, 16.99, 16.99),
(104, 12, 1, 4.25, 4.25);

-- Transaction 105: 2026-11-13
INSERT INTO sales_transactions (transaction_id, customer_id, transaction_date, total_amount, payment_mode, cashier_name)
VALUES (105, 5, '2026-11-13 16:20:00', 154.98, 'Credit Card', 'John Doe');
INSERT INTO sales_details (transaction_id, product_id, quantity_sold, unit_price, subtotal) VALUES
(105, 1, 1, 24.99, 24.99),
(105, 4, 1, 129.99, 129.99);

-- Transaction 106: 2026-11-14
INSERT INTO sales_transactions (transaction_id, customer_id, transaction_date, total_amount, payment_mode, cashier_name)
VALUES (106, 6, '2026-11-14 12:00:00', 44.97, 'UPI', 'Alice Smith');
INSERT INTO sales_details (transaction_id, product_id, quantity_sold, unit_price, subtotal) VALUES
(106, 13, 2, 11.50, 23.00),
(106, 14, 3, 5.99, 17.97),
(106, 15, 1, 4.50, 4.50);

-- Transaction 107: 2026-11-15
INSERT INTO sales_transactions (transaction_id, customer_id, transaction_date, total_amount, payment_mode, cashier_name)
VALUES (107, 7, '2026-11-15 17:35:00', 89.96, 'Cash', 'John Doe');
INSERT INTO sales_details (transaction_id, product_id, quantity_sold, unit_price, subtotal) VALUES
(107, 17, 2, 19.99, 39.98),
(107, 11, 4, 6.49, 25.96),
(107, 20, 2, 13.50, 27.00);

-- Transaction 108: 2026-11-16
INSERT INTO sales_transactions (transaction_id, customer_id, transaction_date, total_amount, payment_mode, cashier_name)
VALUES (108, 8, '2026-11-16 10:45:00', 74.98, 'Credit Card', 'Alice Smith');
INSERT INTO sales_details (transaction_id, product_id, quantity_sold, unit_price, subtotal) VALUES
(108, 2, 1, 79.99, 79.99);

-- Transaction 109: 2026-11-16
INSERT INTO sales_transactions (transaction_id, customer_id, transaction_date, total_amount, payment_mode, cashier_name)
VALUES (109, 9, '2026-11-16 18:25:00', 58.98, 'UPI', 'John Doe');
INSERT INTO sales_details (transaction_id, product_id, quantity_sold, unit_price, subtotal) VALUES
(109, 5, 2, 18.50, 37.00),
(109, 6, 1, 22.00, 22.00);

-- Transaction 110: 2026-11-17
INSERT INTO sales_transactions (transaction_id, customer_id, transaction_date, total_amount, payment_mode, cashier_name)
VALUES (110, 10, '2026-11-17 11:15:00', 82.47, 'Debit Card', 'Alice Smith');
INSERT INTO sales_details (transaction_id, product_id, quantity_sold, unit_price, subtotal) VALUES
(110, 1, 2, 24.99, 49.98),
(110, 3, 2, 12.99, 25.98),
(110, 12, 1, 4.25, 4.25);

-- Transaction 111: 2026-11-17
INSERT INTO sales_transactions (transaction_id, customer_id, transaction_date, total_amount, payment_mode, cashier_name)
VALUES (111, 1, '2026-11-17 16:50:00', 50.97, 'UPI', 'John Doe');
INSERT INTO sales_details (transaction_id, product_id, quantity_sold, unit_price, subtotal) VALUES
(111, 9, 3, 16.99, 50.97);

-- Transaction 112: 2026-11-18 (Today's Sales)
INSERT INTO sales_transactions (transaction_id, customer_id, transaction_date, total_amount, payment_mode, cashier_name)
VALUES (112, 2, '2026-11-18 09:30:00', 69.97, 'Cash', 'Alice Smith');
INSERT INTO sales_details (transaction_id, product_id, quantity_sold, unit_price, subtotal) VALUES
(112, 18, 1, 34.99, 34.99),
(112, 19, 2, 7.99, 15.98),
(112, 20, 1, 13.50, 13.50);

-- Transaction 113: 2026-11-18 (Today's Sales)
INSERT INTO sales_transactions (transaction_id, customer_id, transaction_date, total_amount, payment_mode, cashier_name)
VALUES (113, 3, '2026-11-18 14:15:00', 99.98, 'Credit Card', 'John Doe');
INSERT INTO sales_details (transaction_id, product_id, quantity_sold, unit_price, subtotal) VALUES
(113, 1, 2, 24.99, 49.98),
(113, 3, 3, 12.99, 38.97);

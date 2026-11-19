-- ==============================================================================
-- 04_master_setup.sql: Complete Master Database Setup Script
-- Retail Store Inventory and Sales Analysis System
-- Course: 25ITT31 - Database Management Systems (VCET R2025)
-- Register No: 9, 39, 69, 99
-- ==============================================================================

PRAGMA foreign_keys = ON;

-- ------------------------------------------------------------------------------
-- PART 1: SCHEMA DDL (Table Definitions & Constraints)
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS stock_updates;
DROP TABLE IF EXISTS sales_details;
DROP TABLE IF EXISTS sales_transactions;
DROP TABLE IF EXISTS inventory;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS categories;

DROP TRIGGER IF EXISTS trg_prevent_oversale;
DROP TRIGGER IF EXISTS trg_deduct_stock_on_sale;
DROP TRIGGER IF EXISTS trg_audit_restock;

DROP VIEW IF EXISTS v_daily_sales_summary;
DROP VIEW IF EXISTS v_low_stock_alerts;
DROP VIEW IF EXISTS v_product_sales_performance;
DROP VIEW IF EXISTS v_category_revenue;

CREATE TABLE categories (
    category_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name   TEXT NOT NULL UNIQUE,
    description     TEXT
);

CREATE TABLE products (
    product_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name    TEXT NOT NULL,
    category_id     INTEGER NOT NULL,
    unit_price      REAL NOT NULL CHECK(unit_price > 0),
    cost_price      REAL NOT NULL CHECK(cost_price > 0 AND cost_price <= unit_price),
    reorder_level   INTEGER NOT NULL DEFAULT 10 CHECK(reorder_level >= 0),
    created_at      TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE customers (
    customer_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name   TEXT NOT NULL,
    phone           TEXT NOT NULL UNIQUE CHECK(LENGTH(phone) >= 10),
    email           TEXT CHECK(email LIKE '%@%._%'),
    address         TEXT,
    registration_date TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE inventory (
    inventory_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id      INTEGER NOT NULL UNIQUE,
    available_stock INTEGER NOT NULL DEFAULT 0 CHECK(available_stock >= 0),
    last_updated    TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE sales_transactions (
    transaction_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id      INTEGER NOT NULL,
    transaction_date TEXT NOT NULL DEFAULT (DATETIME('now', 'localtime')),
    total_amount     REAL NOT NULL DEFAULT 0.0 CHECK(total_amount >= 0),
    payment_mode     TEXT NOT NULL CHECK(payment_mode IN ('Cash', 'Credit Card', 'Debit Card', 'UPI')),
    cashier_name     TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE sales_details (
    detail_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_id  INTEGER NOT NULL,
    product_id      INTEGER NOT NULL,
    quantity_sold   INTEGER NOT NULL CHECK(quantity_sold > 0),
    unit_price      REAL NOT NULL CHECK(unit_price > 0),
    subtotal        REAL NOT NULL CHECK(subtotal >= 0),
    FOREIGN KEY (transaction_id) REFERENCES sales_transactions(transaction_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE stock_updates (
    update_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id      INTEGER NOT NULL,
    change_quantity INTEGER NOT NULL,
    update_type     TEXT NOT NULL CHECK(update_type IN ('SALE', 'RESTOCK', 'ADJUSTMENT', 'RETURN', 'INITIAL')),
    balance_stock   INTEGER NOT NULL CHECK(balance_stock >= 0),
    update_timestamp TEXT DEFAULT (DATETIME('now', 'localtime')),
    notes           TEXT,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

-- Performance Indexes
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_inventory_product ON inventory(product_id);
CREATE INDEX idx_sales_date ON sales_transactions(transaction_date);
CREATE INDEX idx_sales_details_tx ON sales_details(transaction_id);
CREATE INDEX idx_sales_details_prod ON sales_details(product_id);

-- ------------------------------------------------------------------------------
-- PART 2: TRIGGERS & ANALYTICAL VIEWS
-- ------------------------------------------------------------------------------
CREATE TRIGGER trg_prevent_oversale
BEFORE INSERT ON sales_details
FOR EACH ROW
WHEN NEW.quantity_sold > (SELECT available_stock FROM inventory WHERE product_id = NEW.product_id)
BEGIN
    SELECT RAISE(ABORT, 'INSUFFICIENT_STOCK_ERROR: Requested quantity exceeds available inventory stock!');
END;

CREATE TRIGGER trg_deduct_stock_on_sale
AFTER INSERT ON sales_details
FOR EACH ROW
BEGIN
    UPDATE inventory 
    SET available_stock = available_stock - NEW.quantity_sold,
        last_updated = DATETIME('now', 'localtime')
    WHERE product_id = NEW.product_id;

    INSERT INTO stock_updates (product_id, change_quantity, update_type, balance_stock, notes)
    VALUES (
        NEW.product_id, 
        -NEW.quantity_sold, 
        'SALE', 
        (SELECT available_stock FROM inventory WHERE product_id = NEW.product_id),
        'Auto stock deduction for Sales Transaction #' || NEW.transaction_id || ' (Qty: ' || NEW.quantity_sold || ')'
    );
END;

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

-- ------------------------------------------------------------------------------
-- PART 3: SAMPLE DATA SEEDING
-- ------------------------------------------------------------------------------
INSERT INTO categories (category_id, category_name, description) VALUES
(1, 'Electronics', 'Consumer electronics, accessories, smart devices, and peripherals'),
(2, 'Groceries & Staples', 'Daily grocery staples, rice, flour, pulses, cooking oils, and condiments'),
(3, 'Beverages & Snacks', 'Packaged juices, organic tea, roasted coffees, sodas, and cookies'),
(4, 'Personal Care', 'Hygiene essentials, skincare, haircare, sanitizers, and soaps'),
(5, 'Home & Kitchen', 'Cookware, cleaning agents, organizers, and tableware');

INSERT INTO products (product_id, product_name, category_id, unit_price, cost_price, reorder_level) VALUES
(1, 'Wireless Optical Mouse', 1, 24.99, 14.50, 15),
(2, 'Mechanical Gaming Keyboard', 1, 79.99, 45.00, 10),
(3, 'USB-C Fast Charging Cable', 1, 12.99, 5.20, 20),
(4, 'Noise Cancelling Headphones', 1, 129.99, 75.00, 8),
(5, 'Basmati Rice Premium (5kg)', 2, 18.50, 13.00, 25),
(6, 'Organic Wheat Flour (10kg)', 2, 22.00, 16.50, 20),
(7, 'Extra Virgin Olive Oil (1L)', 2, 14.99, 9.80, 12),
(8, 'Pure Golden Honey (500g)', 2, 8.50, 5.00, 15),
(9, 'Arabica Dark Roast Coffee Beans (500g)', 3, 16.99, 10.50, 12),
(10, 'Organic Green Tea (100 Bags)', 3, 9.99, 5.50, 18),
(11, 'Almond Butter Crunch Granola (400g)', 3, 6.49, 3.80, 15),
(12, 'Natural Coconut Water (1L)', 3, 4.25, 2.50, 30),
(13, 'Botanical Moisturizing Shampoo (400ml)', 4, 11.50, 6.20, 15),
(14, 'Antibacterial Hand Wash (500ml)', 4, 5.99, 3.10, 25),
(15, 'Charcoal Whitening Toothpaste (150g)', 4, 4.50, 2.20, 20),
(16, 'Moisturizing Aloe Vera Lotion (250ml)', 4, 8.99, 4.50, 10),
(17, 'Stainless Steel Thermal Flask (1L)', 5, 19.99, 11.00, 10),
(18, 'Non-Stick Ceramic Frying Pan (28cm)', 5, 34.99, 21.00, 8),
(19, 'Microfiber Cleaning Cloth Set (6pk)', 5, 7.99, 3.50, 20),
(20, 'Aromatherapy Soy Scented Candle', 5, 13.50, 6.80, 12);

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

INSERT INTO inventory (inventory_id, product_id, available_stock, last_updated) VALUES
(1, 1, 65, '2026-11-01 09:00:00'),
(2, 2, 38, '2026-11-01 09:00:00'),
(3, 3, 90, '2026-11-01 09:00:00'),
(4, 4, 5,  '2026-11-01 09:00:00'),
(5, 5, 75, '2026-11-01 09:00:00'),
(6, 6, 50, '2026-11-01 09:00:00'),
(7, 7, 40, '2026-11-01 09:00:00'),
(8, 8, 45, '2026-11-01 09:00:00'),
(9, 9, 35, '2026-11-01 09:00:00'),
(10, 10, 60, '2026-11-01 09:00:00'),
(11, 11, 40, '2026-11-01 09:00:00'),
(12, 12, 8,  '2026-11-01 09:00:00'),
(13, 13, 50, '2026-11-01 09:00:00'),
(14, 14, 80, '2026-11-01 09:00:00'),
(15, 15, 65, '2026-11-01 09:00:00'),
(16, 16, 30, '2026-11-01 09:00:00'),
(17, 17, 28, '2026-11-01 09:00:00'),
(18, 18, 4,  '2026-11-01 09:00:00'),
(19, 19, 55, '2026-11-01 09:00:00'),
(20, 20, 32, '2026-11-01 09:00:00');

INSERT INTO stock_updates (product_id, change_quantity, update_type, balance_stock, update_timestamp, notes)
SELECT product_id, available_stock, 'INITIAL', available_stock, last_updated, 'Opening stock initialization'
FROM inventory;

-- Insert Historical Sales
INSERT INTO sales_transactions (transaction_id, customer_id, transaction_date, total_amount, payment_mode, cashier_name)
VALUES (101, 1, '2026-11-10 10:15:00', 104.98, 'Credit Card', 'John Doe');
INSERT INTO sales_details (transaction_id, product_id, quantity_sold, unit_price, subtotal) VALUES
(101, 1, 1, 24.99, 24.99),
(101, 2, 1, 79.99, 79.99);

INSERT INTO sales_transactions (transaction_id, customer_id, transaction_date, total_amount, payment_mode, cashier_name)
VALUES (102, 2, '2026-11-11 11:30:00', 55.49, 'UPI', 'Alice Smith');
INSERT INTO sales_details (transaction_id, product_id, quantity_sold, unit_price, subtotal) VALUES
(102, 5, 2, 18.50, 37.00),
(102, 8, 1, 8.50, 8.50),
(102, 10, 1, 9.99, 9.99);

INSERT INTO sales_transactions (transaction_id, customer_id, transaction_date, total_amount, payment_mode, cashier_name)
VALUES (103, 3, '2026-11-11 15:45:00', 64.95, 'Cash', 'John Doe');
INSERT INTO sales_details (transaction_id, product_id, quantity_sold, unit_price, subtotal) VALUES
(103, 3, 5, 12.99, 64.95);

INSERT INTO sales_transactions (transaction_id, customer_id, transaction_date, total_amount, payment_mode, cashier_name)
VALUES (104, 4, '2026-11-12 14:10:00', 50.98, 'Debit Card', 'Alice Smith');
INSERT INTO sales_details (transaction_id, product_id, quantity_sold, unit_price, subtotal) VALUES
(104, 7, 2, 14.99, 29.98),
(104, 9, 1, 16.99, 16.99),
(104, 12, 1, 4.25, 4.25);

INSERT INTO sales_transactions (transaction_id, customer_id, transaction_date, total_amount, payment_mode, cashier_name)
VALUES (105, 5, '2026-11-13 16:20:00', 154.98, 'Credit Card', 'John Doe');
INSERT INTO sales_details (transaction_id, product_id, quantity_sold, unit_price, subtotal) VALUES
(105, 1, 1, 24.99, 24.99),
(105, 4, 1, 129.99, 129.99);

INSERT INTO sales_transactions (transaction_id, customer_id, transaction_date, total_amount, payment_mode, cashier_name)
VALUES (106, 6, '2026-11-14 12:00:00', 44.97, 'UPI', 'Alice Smith');
INSERT INTO sales_details (transaction_id, product_id, quantity_sold, unit_price, subtotal) VALUES
(106, 13, 2, 11.50, 23.00),
(106, 14, 3, 5.99, 17.97),
(106, 15, 1, 4.50, 4.50);

INSERT INTO sales_transactions (transaction_id, customer_id, transaction_date, total_amount, payment_mode, cashier_name)
VALUES (107, 7, '2026-11-15 17:35:00', 89.96, 'Cash', 'John Doe');
INSERT INTO sales_details (transaction_id, product_id, quantity_sold, unit_price, subtotal) VALUES
(107, 17, 2, 19.99, 39.98),
(107, 11, 4, 6.49, 25.96),
(107, 20, 2, 13.50, 27.00);

INSERT INTO sales_transactions (transaction_id, customer_id, transaction_date, total_amount, payment_mode, cashier_name)
VALUES (108, 8, '2026-11-16 10:45:00', 74.98, 'Credit Card', 'Alice Smith');
INSERT INTO sales_details (transaction_id, product_id, quantity_sold, unit_price, subtotal) VALUES
(108, 2, 1, 79.99, 79.99);

INSERT INTO sales_transactions (transaction_id, customer_id, transaction_date, total_amount, payment_mode, cashier_name)
VALUES (109, 9, '2026-11-16 18:25:00', 58.98, 'UPI', 'John Doe');
INSERT INTO sales_details (transaction_id, product_id, quantity_sold, unit_price, subtotal) VALUES
(109, 5, 2, 18.50, 37.00),
(109, 6, 1, 22.00, 22.00);

INSERT INTO sales_transactions (transaction_id, customer_id, transaction_date, total_amount, payment_mode, cashier_name)
VALUES (110, 10, '2026-11-17 11:15:00', 82.47, 'Debit Card', 'Alice Smith');
INSERT INTO sales_details (transaction_id, product_id, quantity_sold, unit_price, subtotal) VALUES
(110, 1, 2, 24.99, 49.98),
(110, 3, 2, 12.99, 25.98),
(110, 12, 1, 4.25, 4.25);

INSERT INTO sales_transactions (transaction_id, customer_id, transaction_date, total_amount, payment_mode, cashier_name)
VALUES (111, 1, '2026-11-17 16:50:00', 50.97, 'UPI', 'John Doe');
INSERT INTO sales_details (transaction_id, product_id, quantity_sold, unit_price, subtotal) VALUES
(111, 9, 3, 16.99, 50.97);

INSERT INTO sales_transactions (transaction_id, customer_id, transaction_date, total_amount, payment_mode, cashier_name)
VALUES (112, 2, '2026-11-18 09:30:00', 64.47, 'Cash', 'Alice Smith');
INSERT INTO sales_details (transaction_id, product_id, quantity_sold, unit_price, subtotal) VALUES
(112, 18, 1, 34.99, 34.99),
(112, 19, 2, 7.99, 15.98),
(112, 20, 1, 13.50, 13.50);

INSERT INTO sales_transactions (transaction_id, customer_id, transaction_date, total_amount, payment_mode, cashier_name)
VALUES (113, 3, '2026-11-18 14:15:00', 88.95, 'Credit Card', 'John Doe');
INSERT INTO sales_details (transaction_id, product_id, quantity_sold, unit_price, subtotal) VALUES
(113, 1, 2, 24.99, 49.98),
(113, 3, 3, 12.99, 38.97);

-- ==============================================================================
-- 01_schema_ddl.sql: Relational Table Creation Scripts with Integrity Constraints
-- Retail Store Inventory and Sales Analysis System
-- Course: 25ITT31 - Database Management Systems (VCET R2025)
-- Register No: 9, 39, 69, 99
-- ==============================================================================

PRAGMA foreign_keys = ON;

-- Drop existing tables to allow clean re-execution
DROP TABLE IF EXISTS stock_updates;
DROP TABLE IF EXISTS sales_details;
DROP TABLE IF EXISTS sales_transactions;
DROP TABLE IF EXISTS inventory;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS categories;

-- ------------------------------------------------------------------------------
-- 1. Table: categories (Product taxonomy classifications)
-- ------------------------------------------------------------------------------
CREATE TABLE categories (
    category_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name   TEXT NOT NULL UNIQUE,
    description     TEXT
);

-- ------------------------------------------------------------------------------
-- 2. Table: products (Catalog items with pricing and reorder thresholds)
-- ------------------------------------------------------------------------------
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

-- ------------------------------------------------------------------------------
-- 3. Table: customers (Registered shoppers and POS contact registry)
-- ------------------------------------------------------------------------------
CREATE TABLE customers (
    customer_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name   TEXT NOT NULL,
    phone           TEXT NOT NULL UNIQUE CHECK(LENGTH(phone) >= 10),
    email           TEXT CHECK(email LIKE '%@%._%'),
    address         TEXT,
    registration_date TEXT DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------------------------
-- 4. Table: inventory (Real-time on-hand stock per product)
-- ------------------------------------------------------------------------------
CREATE TABLE inventory (
    inventory_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id      INTEGER NOT NULL UNIQUE,
    available_stock INTEGER NOT NULL DEFAULT 0 CHECK(available_stock >= 0),
    last_updated    TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

-- ------------------------------------------------------------------------------
-- 5. Table: sales_transactions (Header invoices for billing transactions)
-- ------------------------------------------------------------------------------
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

-- ------------------------------------------------------------------------------
-- 6. Table: sales_details (Itemized line items belonging to sales transactions)
-- ------------------------------------------------------------------------------
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

-- ------------------------------------------------------------------------------
-- 7. Table: stock_updates (Immutable audit trail of all inventory modifications)
-- ------------------------------------------------------------------------------
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

-- Indexes for performance optimization (DBMS Unit 2/3)
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_inventory_product ON inventory(product_id);
CREATE INDEX idx_sales_date ON sales_transactions(transaction_date);
CREATE INDEX idx_sales_details_tx ON sales_details(transaction_id);
CREATE INDEX idx_sales_details_prod ON sales_details(product_id);

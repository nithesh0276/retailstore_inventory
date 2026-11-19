# Database Data Dictionary and Table Structures

**Course:** 25ITT31 - Database Management Systems (Unit 1 & Unit 2)  
**Database File:** `retail_store.db` (SQLite 3 ACID-compliant relational database)  

---

## 1. Table: `categories`
Stores standardized classification buckets for retail store products.

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `category_id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique system-generated category identifier |
| `category_name` | TEXT | NOT NULL, UNIQUE | Human-readable category label (e.g., Electronics) |
| `description` | TEXT | NULLABLE | Detailed description of the category scope |

---

## 2. Table: `products`
Master catalog containing product attributes, pricing, and reorder levels.

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `product_id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique product SKU identifier |
| `product_name` | TEXT | NOT NULL | Commercial product name |
| `category_id` | INTEGER | NOT NULL, FK $\to$ `categories(category_id)` | Foreign key link to taxonomy category |
| `unit_price` | REAL | NOT NULL, CHECK(`unit_price` > 0) | Selling price per unit charged to customer |
| `cost_price` | REAL | NOT NULL, CHECK(`cost_price` > 0 AND $\le$ `unit_price`) | Procurement / purchase cost per unit |
| `reorder_level` | INTEGER | NOT NULL, DEFAULT 10, CHECK($\ge$ 0) | Minimum stock threshold triggering restock |
| `created_at` | TEXT | DEFAULT CURRENT_TIMESTAMP | Product entry timestamp |

---

## 3. Table: `customers`
Registry of registered store shoppers for sales association.

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `customer_id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique customer identification number |
| `customer_name` | TEXT | NOT NULL | Customer's full name |
| `phone` | TEXT | NOT NULL, UNIQUE, CHECK(LENGTH $\ge$ 10) | Primary 10-digit phone contact number |
| `email` | TEXT | CHECK(`email` LIKE '%@%._%') | Electronic mail address |
| `address` | TEXT | NULLABLE | Physical residential / delivery address |
| `registration_date` | TEXT | DEFAULT CURRENT_TIMESTAMP | Registration timestamp |

---

## 4. Table: `inventory`
Real-time tracking of on-hand inventory stock per product.

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `inventory_id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique inventory ledger identifier |
| `product_id` | INTEGER | NOT NULL, UNIQUE, FK $\to$ `products(product_id)` | 1:1 foreign key reference to product |
| `available_stock` | INTEGER | NOT NULL, DEFAULT 0, CHECK($\ge$ 0) | Current physically available units on shelf |
| `last_updated` | TEXT | DEFAULT CURRENT_TIMESTAMP | Timestamp of most recent stock adjustment |

---

## 5. Table: `sales_transactions`
Invoice headers capturing point-of-sale customer checkouts.

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `transaction_id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique invoice receipt transaction number |
| `customer_id` | INTEGER | NOT NULL, FK $\to$ `customers(customer_id)` | Customer to whom order is billed |
| `transaction_date` | TEXT | NOT NULL, DEFAULT (DATETIME('now','localtime')) | Date and time sale was finalized |
| `total_amount` | REAL | NOT NULL, CHECK($\ge$ 0) | Net payable bill amount |
| `payment_mode` | TEXT | NOT NULL, CHECK(IN 'Cash','Credit Card','Debit Card','UPI') | Mode of payment settled |
| `cashier_name` | TEXT | NOT NULL | Name of billing counter operator |

---

## 6. Table: `sales_details`
Itemized line items recording specific products and quantities in each sale.

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `detail_id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique line item record identifier |
| `transaction_id` | INTEGER | NOT NULL, FK $\to$ `sales_transactions(transaction_id)` | Parent transaction invoice link |
| `product_id` | INTEGER | NOT NULL, FK $\to$ `products(product_id)` | Product purchased |
| `quantity_sold` | INTEGER | NOT NULL, CHECK(`quantity_sold` > 0) | Quantity purchased in this line item |
| `unit_price` | REAL | NOT NULL, CHECK(`unit_price` > 0) | Unit price locked at time of sale |
| `subtotal` | REAL | NOT NULL, CHECK(`subtotal` $\ge$ 0) | Line subtotal (`quantity_sold` * `unit_price`) |

---

## 7. Table: `stock_updates`
Immutable audit log recording every inventory modification event.

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `update_id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique audit entry identifier |
| `product_id` | INTEGER | NOT NULL, FK $\to$ `products(product_id)` | Product whose stock was modified |
| `change_quantity` | INTEGER | NOT NULL | Signed delta (- for sale, + for restock) |
| `update_type` | TEXT | NOT NULL, CHECK(IN 'SALE','RESTOCK','ADJUSTMENT','RETURN','INITIAL') | Classification of stock event |
| `balance_stock` | INTEGER | NOT NULL, CHECK($\ge$ 0) | Resulting available stock balance |
| `update_timestamp` | TEXT | DEFAULT (DATETIME('now','localtime')) | Precise timestamp of modification |
| `notes` | TEXT | NULLABLE | Human or system notes describing event |

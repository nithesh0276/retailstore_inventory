# Software Requirements Specification (SRS)
## Retail Store Inventory and Sales Analysis System
**Document Version:** 1.0  
**Standard:** IEEE Std 830-1998  
**Department:** Department of Information Technology, VCET (R2025 Regulation)  
**Course:** 25ITT33 - Software Engineering  
**Register Numbers:** 9, 39, 69, 99  

---

## 1. Introduction

### 1.1 Purpose
This Software Requirements Specification (SRS) provides a comprehensive description of the **Retail Store Inventory and Sales Analysis System**. It outlines the functional and non-functional requirements, external interfaces, system architectural constraints, and verification criteria for developers, database administrators, data scientists, and evaluators.

### 1.2 Document Conventions
- **FR-#**: Functional Requirement identifier.
- **NFR-#**: Non-Functional Requirement identifier.
- **DB-#**: Database Requirement identifier.
- **Priority**: High (Must-have for operational release), Medium (Desirable for full utility), Low (Future enhancement).
- Font conventions: Monospace font denotes database tables, SQL queries, classes, or code variables.

### 1.3 Intended Audience and Reading Suggestions
This document is targeted toward:
1. **Academic Evaluators and Faculty:** To verify syllabus mapping to 25ITT33, 25ITT31, 25ITT32, and 25ITC31.
2. **Software Engineers and Developers:** To implement object-oriented Java modules and transactional logic.
3. **Database Engineers:** To construct the 3NF relational schema, integrity triggers, and analytical views.
4. **Data Analysts:** To build the Python ETL, statistical wrangling, and Matplotlib/Seaborn dashboards.

### 1.4 Project Scope
The Retail Store Inventory and Sales Analysis System is an enterprise desktop application designed to eliminate inventory discrepancies, streamline retail counter checkout, guarantee stock integrity, generate operational reports, and extract business intelligence through predictive and descriptive visualizations.

### 1.5 References
1. Roger S. Pressman & Bruce R. Maxim, *Software Engineering: A Practitioner's Approach*, 9th Edition, McGraw-Hill, 2020.
2. Ian Sommerville, *Software Engineering*, 10th Edition, Pearson, 2023.
3. Abraham Silberschatz, Henry F. Korth, S. Sudarshan, *Database System Concepts*, 7th Edition, 2020.
4. Herbert Schildt, *Java: The Complete Reference*, 13th Edition, McGraw-Hill, 2024.
5. IEEE Recommended Practice for Software Requirements Specifications (IEEE Std 830-1998).

---

## 2. Overall Description

### 2.1 Product Perspective
The system operates as a multi-tier client-server/desktop enterprise architecture:
```
[ Presentation Tier ]  --> Java CLI/Console Dashboard + Python Visualization Suite
         ↓
[ Business Logic Tier ] --> Java Services (SalesService, InventoryService, ReportService)
         ↓
[ Data Access Tier ]   --> JDBC Layer (DAO Pattern) + Python SQLite3 Connector
         ↓
[ Database Storage ]   --> Relational Database (retail_store.db with Triggers & Views)
```

### 2.2 Product Functions
The core capabilities of the system include:
1. **Catalog & Product Management:** Registering categories and products with price, stock, and reorder levels.
2. **Customer Registry:** Maintaining customer profiles, contact numbers, and purchase histories.
3. **Point of Sale (POS) Checkout:** Processing itemized sales with multi-product billing, customer attribution, and payment mode tracking.
4. **Stock Availability Validation:** Pre-verifying inventory before order confirmation; blocking over-sales.
5. **Real-Time Automated Stock Decrement:** Updating physical stock atomically upon sale commitment via database triggers and DAO transactions.
6. **Stock Movement Audit Logging:** Recording every inventory change (Sale, Restock, Return, Adjustment).
7. **Operational Reporting:** Generating daily sales summaries, low-stock alerts, and category distributions.
8. **Python Exploratory Data Analysis & Visualization:** Extracting data, cleaning outliers/nulls, and rendering 7 analytical visual charts.

### 2.3 User Classes and Characteristics
- **Store Manager (Admin):** Full privileges for product catalog updates, pricing adjustments, inventory restocking, and viewing executive analytical reports.
- **Cashier / Sales Clerk:** Privileges to record customer sales, check real-time stock availability, and print transaction receipts.
- **Inventory Auditor:** Privileges to inspect low-stock items, reconcile stock discrepancies, and log supplier restocks.
- **Data Analyst:** Privileges to extract raw operational tables, run Python preprocessing pipelines, and generate exploratory data visualizations.

### 2.4 Operating Environment
- **Operating System:** Microsoft Windows 10 / 11 (64-bit).
- **Java Runtime:** Java Development Kit (JDK) 21 or 25.
- **Python Environment:** Python 3.12+ with NumPy, Pandas, Matplotlib, Seaborn.
- **Database Engine:** SQLite 3.45+ (Self-contained, ACID compliant, embedded).
- **Execution Interface:** Windows Batch Scripts (`.bat`) and Command Console.

### 2.5 Design and Implementation Constraints
1. **Zero External Server Dependency:** Database must be self-contained in a portable file (`retail_store.db`) to enable friction-free academic evaluation without network port collisions.
2. **Strict Transactional Integrity:** A sale transaction and its stock reduction must execute atomically. Partial commits are strictly forbidden.
3. **Declarative and Procedural Stock Checks:** Over-sale prevention must be enforced at both the Java application layer (Custom Exception) and the Database layer (Trigger `BEFORE INSERT`).

---

## 3. Specific Requirements

### 3.1 External Interface Requirements
#### 3.1.1 User Interfaces
- Console-based command dashboard formatted with UTF-8 border framing, tabular reports, and colorized transaction status.
- High-resolution graphical user interface output for data science charts rendered and saved as PNG files.

#### 3.1.2 Software Interfaces
- **Java Database Connectivity (JDBC):** SQLite JDBC driver (`sqlite-jdbc-3.45.2.0.jar`) managing connections, transactions, and statements.
- **Python SQLite3 Engine:** Native Python C-based connector for Pandas DataFrame queries.

### 3.2 Functional Requirements

#### FR-01: Product Details & Category Management
- **Description:** The system shall allow authorized users to create, update, view, and delete product categories and product records.
- **Inputs:** Product Name, Category ID, Unit Price (float > 0), Cost Price (float > 0), Initial Stock (int >= 0), Reorder Level (int >= 0).
- **Outputs:** Generated unique Product ID, success/failure notification, updated product list.
- **Validation:** Unit price must be strictly greater than cost price; product name must be non-empty and unique within category.

#### FR-02: Customer Profile Management
- **Description:** The system shall record customer identifiers, full names, phone numbers, email addresses, and shipping/billing addresses.
- **Inputs:** Customer Name, Phone Number (unique, 10-digit format), Email, Address.
- **Outputs:** Unique Customer ID.

#### FR-03: Sales Transaction Recording
- **Description:** The system shall capture multi-line sales transactions containing multiple products, quantities, prices, discounts, and payment methods.
- **Inputs:** Customer ID, List of (Product ID, Quantity), Payment Mode (Cash, Credit Card, UPI, Debit Card), Cashier Name.
- **Outputs:** Itemized transaction invoice, total payable amount, transaction timestamp.

#### FR-04: Stock Availability Verification & Over-Sale Prevention
- **Description:** Before persisting a sale transaction, the system must verify whether `available_stock >= requested_quantity` for every item.
- **Response to Violation:** If any item's requested quantity exceeds available stock, the entire transaction is rejected with an `InsufficientStockException`, displaying the available quantity and required quantity. Database triggers act as a secondary defensive barrier.

#### FR-05: Real-Time Automatic Stock Deduction & Movement Audit
- **Description:** Upon successful transaction recording, available stock in the `inventory` table must immediately decrement by the sold quantity. A corresponding audit record must be inserted into `stock_updates` capturing `(product_id, change_quantity, update_type='SALE', balance_stock, timestamp)`.

#### FR-06: Operational Reporting Suite
- **Description:** The system shall produce real-time operational reports:
  - *Daily Sales Summary:* Date, Total Orders, Total Revenue, Average Order Value.
  - *Product Availability Report:* Product ID, Name, Category, Unit Price, On-Hand Stock, Stock Value.
  - *Low Stock Alert Report:* Filter items where `available_stock <= reorder_level` with recommended reorder quantities.

#### FR-07: Python Data Science Extraction, Preprocessing & Visualization
- **Description:** The system shall pull transactional and inventory records into Python, clean missing values and duplicates, compute descriptive statistics, and plot 7 designated analytical visualizations.

---

## 4. Non-Functional Requirements (NFRs)

### 4.1 Performance Requirements
- **NFR-01 (Response Time):** Transaction checkout and stock deduction must complete within 200 milliseconds.
- **NFR-02 (Data Pipeline Latency):** Python data extraction, preprocessing, and 7-chart generation pipeline must execute within 5 seconds.

### 4.2 Security Requirements
- **NFR-03 (Data Integrity):** Foreign key constraints must enforce referential integrity (`ON DELETE RESTRICT ON UPDATE CASCADE`).
- **NFR-04 (SQL Injection Prevention):** All database interactions in Java must use parameterized `PreparedStatement`.

### 4.3 Reliability & Availability
- **NFR-05 (ACID Compliance):** Transactions must adhere strictly to Atomicity, Consistency, Isolation, and Durability.
- **NFR-06 (Crash Recovery):** In the event of an unhandled crash or power loss during checkout, the database write-ahead log (WAL) must restore the last consistent state without stock corruption.

### 4.4 Usability & Maintainability
- **NFR-07 (Modularity):** The codebase must strictly decouple Presentation, Service, DAO, and Model layers.
- **NFR-08 (Zero-Config Execution):** Runnable `.bat` scripts must allow instant execution without manual classpath configuration.

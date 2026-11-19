# Requirement Classification and Academic Syllabus Mapping

**Scenario 9: Retail Store Inventory and Sales Analysis System**  
**Academic Regulation:** VCET B.Tech. - Information Technology (R2025)  
**Assigned Register Numbers:** 9, 39, 69, 99  

---

## 1. Executive Summary & Problem Context

In a modern retail enterprise, manual management of product inventories, sales counters, customer transactions, and stock updates leads to critical operational bottlenecks:
- Discrepancies between physical shelf stock and recorded ledger stock.
- Lack of stock availability verification during billing, causing unfulfillable customer orders.
- Delays in identifying fast-moving consumer goods (FMCG) versus sluggish stock.
- Lack of proactive automated alerts for items dipping below safety/reorder thresholds.
- Fragmented transactional records that cannot provide immediate business intelligence or visual sales performance trends.

The **Retail Store Inventory and Sales Analysis System** is engineered as a unified, robust, multi-tier enterprise solution integrating **Software Engineering (25ITT33)** methodologies, **Database Management Systems (25ITT31)** transactional consistency, **Java Programming (25ITT32)** business logic and object-oriented control, and **Foundations of Data Science (25ITC31)** exploratory data analysis and visual forecasting.

---

## 2. Comprehensive Requirement Classification Matrix

Each functional requirement (FR-01 to FR-06) and non-functional requirement (NFR) from the problem scenario has been analyzed against the official academic syllabi and mapped to specific course units, theoretical concepts, and implementation artifacts.

| Req ID | Requirement Description | Primary Subject | Syllabus Course Code & Unit | Specific Syllabus Concepts Mapped | Implementation Deliverables |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **FR-01** | **Maintain Product Details**<br>• Product ID, name, category, unit price, cost price, available stock, reorder levels.<br>• CRUD operations on products. | **Database Management System** & **Java Programming** | **25ITT31 (Unit 1, Unit 2)**<br>**25ITT32 (Unit 1, Unit 2, Unit 4)** | • Relational Model, Keys, Integrity Constraints (Primary Key, Foreign Key, NOT NULL, CHECK).<br>• Java Classes, Encapsulation, Methods, Constructors, JDBC PreparedStatement, String handling. | • Table: `products`, `categories`<br>• Java: `Product.java`, `ProductDAO.java`<br>• Interactive Console Product Manager |
| **FR-02** | **Record Sales Transactions**<br>• Capture transaction ID, customer ID, cashier, payment mode, transaction timestamp.<br>• Line items: product details, quantity sold, unit price, line subtotal. | **Database Management System** & **Java Programming** | **25ITT31 (Unit 2, Unit 4)**<br>**25ITT32 (Unit 3, Unit 4, Unit 5)** | • ACID Properties of Transactions, Multi-table Joins, Intermediate SQL, Foreign Keys.<br>• Java JDBC `setAutoCommit(false)`, `commit()`, `rollback()`, Collections (`List<SalesDetail>`), Exception Handling. | • Tables: `sales_transactions`, `sales_details`<br>• Java: `SalesService.java`, `SalesDAO.java`<br>• Transaction rollback on failure |
| **FR-03** | **Automatic Stock Quantity Updates**<br>• Instantly decrement available stock upon successful sale.<br>• Maintain an immutable audit log of stock movements (Sales, Restocks, Adjustments). | **Database Management System** & **Java Programming** | **25ITT31 (Unit 2 - Advanced SQL)**<br>**25ITT32 (Unit 3 - Exceptions)** | • Database Triggers (`AFTER INSERT ON sales_details`), Constraints, Transactions.<br>• Service Layer Business Logic, Event Logging, Exception propagation. | • Trigger: `trg_deduct_stock_on_sale`<br>• Table: `stock_updates`<br>• Java: `InventoryDAO.java`, `InventoryService.java` |
| **FR-04** | **Check Stock Availability & Prevent Over-sale**<br>• Verify requested quantity against on-hand inventory before sale processing.<br>• Reject transactions exceeding stock with explicit error messages and zero inventory change. | **Software Engineering**, **DBMS**, & **Java Programming** | **25ITT33 (Unit 2, Unit 4)**<br>**25ITT31 (Unit 2 - Triggers/Check)**<br>**25ITT32 (Unit 3 - Exceptions)** | • Requirements Elicitation, Boundary Value Analysis, Negative Testing.<br>• Trigger: `trg_prevent_oversale` (`RAISE(ABORT)` / CHECK constraints).<br>• Custom Java Exception: `InsufficientStockException`. | • Use Case & Activity Decision Node<br>• SQLite Trigger + Java Pre-check<br>• JUnit / Automation Test Suite TC-04 |
| **FR-05** | **Generate Operational Reports**<br>• Daily sales revenue, order counts, average basket size.<br>• Real-time product availability report.<br>• Low-stock items breaching reorder thresholds. | **Database Management System** & **Java Programming** | **25ITT31 (Unit 2 - Views, Aggregate Functions)**<br>**25ITT32 (Unit 5 - Generics, Collections, Lambdas & Streams)** | • SQL Aggregate Functions (`SUM`, `COUNT`, `AVG`), `GROUP BY`, `HAVING`, Database Views.<br>• Java Stream API (`filter()`, `map()`, `sorted()`, `collect(Collectors.toList())`), Lambda expressions. | • Views: `v_daily_sales_summary`, `v_low_stock_alerts`<br>• Java: `ReportService.java`<br>• Terminal tabular report generator |
| **FR-06** | **Data Retrieval, Preprocessing & Python Visualization**<br>• Extract database records into DataFrames.<br>• Clean missing values, duplicates, format types, detect outliers.<br>• Statistical analysis of fast-selling and low-stock items.<br>• Generate charts (Bar, Pie, Line, Heatmap). | **Foundations of Data Science** | **25ITC31 (Unit 1, Unit 2, Unit 3, Unit 4, Unit 5)** | • Unit 1: Data Science Roadmap, Averages, Dispersion.<br>• Unit 2: Python fundamentals, File handling, DB connect.<br>• Unit 3: NumPy arrays, Pandas DataFrames, Grouping, Aggregation.<br>• Unit 4: Data cleaning, Outlier IQR, Feature creation.<br>• Unit 5: EDA, Matplotlib, Seaborn charts. | • Python scripts: `db_extractor.py`, `data_preprocessor.py`, `data_analyzer.py`, `visualizer.py`<br>• 7 High-resolution PNG Visualizations |

---

## 3. Detailed Subject-Wise Responsibility Allocation

### Subject 1: Software Engineering (25ITT33)
- **Scope & Role:** Architectural blueprint, requirements modeling, design diagrams, and quality verification.
- **Syllabus Topic Alignment:**
  - **Unit 1: Software Process:** Adoption of the Iterative & Agile Scrum model for multi-component delivery.
  - **Unit 2: Requirements:** Requirement Elicitation, Specification (IEEE Std 830 SRS), Class-Based Modeling.
  - **Unit 3: Software Design:** System Architecture (4-Layered Architecture), Component-Level Design, Interface Design, UML Diagrams (Use Case, Class, Activity, Sequence, DFD Levels 0, 1, 2).
  - **Unit 4: Software Testing:** Test Strategy, Black Box Testing (Equivalence Partitioning & Boundary Value Analysis for stock thresholds), White Box Testing (Basis Path & Cyclomatic Complexity for checkout logic), Test Case Suite, Defect Logging.
  - **Unit 5: Project Management:** 4P's analysis, LOC & Function Point estimation, Risk assessment.

### Subject 2: Database Management System (25ITT31)
- **Scope & Role:** Relational data architecture, ACID transaction processing, declarative integrity, triggers, and analytical views.
- **Syllabus Topic Alignment:**
  - **Unit 1: Database Systems & Design:** Entity-Relationship (ER) Modeling (Entities: Product, Category, Customer, Sales_Transaction, Sales_Details, Inventory, Stock_Update), Cardinality constraints, Key constraints, Relational Schema design.
  - **Unit 2: SQL:** Complete DDL table definitions with `CHECK`, `NOT NULL`, `UNIQUE`, `FOREIGN KEY ... ON UPDATE CASCADE ON DELETE RESTRICT`. Intermediate SQL: Joins, Subqueries, Aggregate functions, Views (`v_daily_sales_summary`, `v_low_stock_alerts`, `v_product_sales_performance`). Advanced SQL: Automated triggers (`trg_prevent_oversale`, `trg_deduct_stock_on_sale`, `trg_restock_update`).
  - **Unit 3: Normalization:** Functional Dependency analysis, 1NF, 2NF, 3NF, BCNF validation to eliminate update, insertion, and deletion anomalies.
  - **Unit 4: Transaction Management:** ACID property enforcement, explicit transaction boundaries (`BEGIN TRANSACTION`, `COMMIT`, `ROLLBACK`), isolation, consistency preservation during stock updates.

### Subject 3: Java Programming (25ITT32)
- **Scope & Role:** Object-oriented enterprise application, business validation rules, transactional checkout, exception control, and CLI dashboard.
- **Syllabus Topic Alignment:**
  - **Unit 1: Introduction to Java:** Object-oriented modeling, class fundamentals, encapsulation, method overloading, console I/O formatting.
  - **Unit 2: Inheritance, Packages, Interfaces:** Clean layered package layout (`com.retailstore.model`, `dao`, `service`, `exception`, `util`, `app`), DAO design pattern interface implementation.
  - **Unit 3: Exception Handling & Multithreading:** Custom robust exceptions (`InsufficientStockException`, `ProductNotFoundException`), `try-catch-finally` resource management, atomic transaction boundaries, synchronized stock updates.
  - **Unit 4: String Handling & Database Connection:** JDBC connectivity via SQLite JDBC driver, `PreparedStatement` to prevent SQL injection, `ResultSet` metadata processing, parameter binding.
  - **Unit 5: Generics, Collections, Lambdas & Streams:** Collections (`List`, `Map`, `Set`), Stream API pipelines (`filter`, `sorted`, `map`, `collect`) to calculate business metrics, top selling items, and low stock thresholds.

### Subject 4: Foundations of Data Science (25ITC31)
- **Scope & Role:** Extraction of operational data, data cleaning, statistical modeling, exploratory data analysis (EDA), and graphical visualization.
- **Syllabus Topic Alignment:**
  - **Unit 1: Data Science Fundamentals:** Descriptive statistics (Mean, Median, Standard Deviation, Interquartile Range, Z-scores) for sales revenue and order quantities.
  - **Unit 2: Python Foundations:** Python 3.12 scripting, database connection (`sqlite3`), data structures, CSV/JSON file exports.
  - **Unit 3: Data Wrangling:** NumPy ndarrays, Pandas DataFrames and Series, indexing, grouping, multi-table joining, pivot tables.
  - **Unit 4: Data Cleaning & Transformation:** Missing value imputation, duplicate record removal, data type casting (datetime parsing), IQR outlier detection for sales spikes, feature engineering (Revenue, Profit Margin, Stock-to-Sales Velocity Ratio).
  - **Unit 5: EDA & Visualization Techniques:** Matplotlib and Seaborn visualization suite:
    1. Category-wise product distribution (Pie and Donut chart).
    2. Product-wise sales volume and revenue (Grouped bar chart).
    3. Daily sales trend with 3-day rolling average (Time-series line chart).
    4. Stock availability vs. reorder thresholds (Status comparison bar chart).
    5. Top 5 fast-selling products (Ranked horizontal bar chart).
    6. Low-stock inventory risk matrix (Diverging warning chart).
    7. Feature correlation matrix (Seaborn heatmap).

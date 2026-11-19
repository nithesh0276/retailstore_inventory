# Retail Store Inventory and Sales Analysis System

**Academic Regulation:** VCET B.Tech. - Information Technology (R2025 Regulation)  
**Assigned Register Numbers:** 9, 39, 69, 99  
**Scenario:** Scenario 9 - Retail Store Inventory and Sales Analysis System  

---

## 1. Project Overview & Multi-Disciplinary Architecture

The **Retail Store Inventory and Sales Analysis System** is an enterprise solution designed to automate retail counter billing, eliminate inventory discrepancies, ensure transactional consistency, prevent over-sale conditions, generate operational intelligence reports, and provide data science forecasting visualizations.

The project is classified and implemented across four academic subjects:
1. **Software Engineering (25ITT33):** Requirements analysis, IEEE Std 830 SRS, UML diagrams (Use Case, Class, Activity, Sequence), Data Flow Diagrams (Level 0, 1, 2), System Architecture, and comprehensive testing documentation.
2. **Database Management System (25ITT31):** E-R modeling, 3NF/BCNF relational schema, SQL DDL with constraints, automatic stock reduction triggers, over-sale prevention defense triggers, analytical views, and reporting queries.
3. **Java Programming (25ITT32):** Multi-tier application (Model, DAO, Service, Exception, Util, App), JDBC SQLite connectivity, atomic transaction management, custom exception handling (`InsufficientStockException`), Java 8+ Stream API reporting, interactive console application, and automated demo runner.
4. **Foundation of Data Science (25ITC31):** Automated data extraction, data cleaning, IQR outlier detection, feature engineering, statistical modeling (central tendency, dispersion), and 7 high-resolution Matplotlib/Seaborn visualization charts.

---

## 2. Directory Hierarchy

```
Retail_Store_Inventory_and_Sales_Analysis_System/
│
├── 1_Software_Engineering/
│   ├── Requirement_Analysis/
│   │   └── REQUIREMENT_CLASSIFICATION_AND_MAPPING.md
│   ├── SRS/
│   │   └── SRS_DOCUMENT.md
│   ├── Use_Case_Diagram/
│   │   ├── USE_CASE_SPECIFICATION.md
│   │   └── use_case_diagram.png
│   ├── Class_Diagram/
│   │   ├── CLASS_DIAGRAM_SPECIFICATION.md
│   │   └── class_diagram.png
│   ├── Activity_Diagram/
│   │   ├── ACTIVITY_DIAGRAM_SPECIFICATION.md
│   │   └── activity_diagram.png
│   ├── Sequence_Diagram/
│   │   ├── SEQUENCE_DIAGRAM_SPECIFICATION.md
│   │   └── sequence_diagram.png
│   ├── DFD/
│   │   ├── DFD_SPECIFICATION.md
│   │   └── dfd_diagram.png
│   ├── Architecture_Diagram/
│   │   ├── ARCHITECTURE_DIAGRAM_SPECIFICATION.md
│   │   └── architecture_diagram.png
│   └── Testing_Documentation/
│       └── TESTING_DOCUMENTATION.md
│
├── 2_Database_Management_System/
│   ├── ER_Diagram/
│   │   ├── ER_DIAGRAM_SPECIFICATION.md
│   │   └── er_diagram.png
│   ├── Relational_Schema/
│   │   └── RELATIONAL_SCHEMA_AND_NORMALIZATION.md
│   ├── SQL_Scripts/
│   │   ├── 01_schema_ddl.sql
│   │   ├── 02_triggers_and_views.sql
│   │   ├── 03_sample_data.sql
│   │   └── 04_master_setup.sql
│   ├── Database_Tables/
│   │   └── DATA_DICTIONARY.md
│   ├── Queries/
│   │   ├── 01_basic_queries.sql
│   │   ├── 02_joins_and_aggregations.sql
│   │   ├── 03_subqueries_and_views.sql
│   │   ├── 04_business_reports.sql
│   │   └── 05_trigger_and_constraint_tests.sql
│   ├── Output/
│   │   ├── db_setup_output.txt
│   │   ├── query_execution_output.txt
│   │   ├── trigger_test_output.txt
│   │   ├── db_setup_screenshot.png
│   │   ├── db_queries_screenshot.png
│   │   └── db_trigger_test_screenshot.png
│   ├── BAT_Files/
│   │   ├── run_db_setup.bat
│   │   ├── run_db_queries.bat
│   │   └── test_db_triggers.bat
│   └── retail_store.db
│
├── 3_Java_Programming/
│   ├── Source_Code/
│   │   └── com/retailstore/
│   │       ├── model/ (Category, Product, Customer, Inventory, SalesTransaction, SalesDetail, StockUpdate)
│   │       ├── dao/ (CategoryDAO, ProductDAO, CustomerDAO, InventoryDAO, SalesDAO)
│   │       ├── service/ (SalesService, InventoryService, ReportService)
│   │       ├── exception/ (InsufficientStockException, ProductNotFoundException, DatabaseOperationException)
│   │       ├── util/ (DBConnection, ConsoleFormatter)
│   │       └── app/ (RetailStoreApp, AutomatedDemoRunner)
│   ├── Database_Connectivity/
│   │   ├── DB_CONNECTIVITY_GUIDE.md
│   │   └── db_config.properties
│   ├── lib/
│   │   ├── sqlite-jdbc.jar
│   │   ├── slf4j-api.jar
│   │   └── slf4j-simple.jar
│   ├── Output/
│   │   ├── java_application_output.txt
│   │   ├── stock_validation_test_output.txt
│   │   └── sales_reports_output.txt
│   ├── Screenshots/
│   │   ├── java_main_menu.png
│   │   ├── java_sales_processing_success.png
│   │   ├── java_stock_prevention_error.png
│   │   └── java_inventory_and_reports.png
│   └── BAT_Files/
│       ├── compile_java.bat
│       ├── run_java_app.bat
│       └── run_java_demo.bat
│
└── 4_Foundation_of_Data_Science/
    ├── Python_Source_Code/
    │   ├── db_extractor.py
    │   ├── data_preprocessor.py
    │   ├── data_analyzer.py
    │   ├── visualizer.py
    │   └── run_full_analysis.py
    ├── Data_Preprocessing/
    │   ├── DATA_PREPROCESSING_DOCUMENTATION.md
    │   ├── cleaned_products.csv
    │   ├── cleaned_sales.csv
    │   └── inventory_status.csv
    ├── Data_Analysis/
    │   └── STATISTICAL_ANALYSIS_REPORT.md
    ├── Visualizations/
    │   ├── 1_category_distribution.png
    │   ├── 2_product_sales_volume_and_revenue.png
    │   ├── 3_daily_sales_trends.png
    │   ├── 4_stock_availability_vs_reorder.png
    │   ├── 5_fast_selling_products.png
    │   ├── 6_low_stock_risk_analysis.png
    │   └── 7_correlation_matrix_heatmap.png
    ├── Output/
    │   └── data_science_analysis_output.txt
    ├── Screenshots/
    │   ├── python_preprocessing_screenshot.png
    │   ├── python_eda_analysis_screenshot.png
    │   └── python_visualization_screenshot.png
    └── BAT_Files/
        ├── run_data_preprocessing.bat
        ├── run_data_analysis.bat
        └── run_full_data_science_pipeline.bat
```

---

## 3. Quick Execution Guide (Runnable BAT Files)

All runnable `.bat` files are pre-configured, tested, and self-contained. They can be executed by simply double-clicking them in Windows File Explorer:

### 3.1 Database Management System (`2_Database_Management_System/BAT_Files/`)
1. `run_db_setup.bat`: Initializes `retail_store.db`, creates tables, armed triggers, views, and seeds sample records. Saves log to `Output/db_setup_output.txt`.
2. `run_db_queries.bat`: Executes joins, aggregations, views, and fast-selling queries. Saves log to `Output/query_execution_output.txt`.
3. `test_db_triggers.bat`: Demonstrates automatic stock decrement on sale and over-sale rejection triggers. Saves log to `Output/trigger_test_output.txt`.

### 3.2 Java Programming (`3_Java_Programming/BAT_Files/`)
1. `compile_java.bat`: Compiles all Java source code against `lib/sqlite-jdbc.jar` into `bin/`.
2. `run_java_demo.bat`: Runs the automated demo harness verifying all 12 functional requirements, testing over-sale exception handling, and saving outputs to `Output/java_application_output.txt`.
3. `run_java_app.bat`: Launches the interactive point-of-sale console dashboard for real-time cashier operations.

### 3.3 Foundation of Data Science (`4_Foundation_of_Data_Science/BAT_Files/`)
1. `run_data_preprocessing.bat`: Connects to SQLite DB, cleans nulls/duplicates, detects IQR outliers, engineers features, and exports CSVs.
2. `run_data_analysis.bat`: Computes central tendency, dispersion, category performance, and fast-selling rankings.
3. `run_full_data_science_pipeline.bat`: Master batch file executing extraction, cleaning, analysis, and generating all 7 high-resolution charts in `Visualizations/`. Saves log to `Output/data_science_analysis_output.txt`.

---

## 4. Verification Checklist

- [x] **Requirement Classification:** Formally mapped against official syllabi (25ITT33, 25ITT31, 25ITT32, 25ITC31).
- [x] **Folder Structure:** 4 distinct folders matching exact required hierarchy.
- [x] **Software Engineering Diagrams:** Use Case, Class, Activity, Sequence, DFD Level 0/1/2, Architecture diagrams provided in Markdown/Mermaid and rendered PNG images.
- [x] **E-R Diagram:** Specifically placed inside `2_Database_Management_System/ER_Diagram/`.
- [x] **Database Implementation:** 7 normalized 3NF tables, 3 triggers (`trg_prevent_oversale`, `trg_deduct_stock_on_sale`, `trg_audit_restock`), 4 views, realistic sample data, and complete query suite.
- [x] **Java Application:** Modular package structure, DAO pattern, SQLite JDBC, ACID transaction control, custom exceptions (`InsufficientStockException`), Stream API reporting, interactive CLI, and automated demo runner.
- [x] **Python Data Science:** Pandas extraction, IQR outlier detection, descriptive statistics, feature creation, and 7 Matplotlib/Seaborn visualization charts.
- [x] **Output & Screenshots:** Complete text output files (`.txt`) and console execution screenshots (`.png`) generated for DBMS, Java, and Data Science.
- [x] **Runnable BAT Files:** 3 tested `.bat` files provided in each implementation subject (total of 9 `.bat` files).

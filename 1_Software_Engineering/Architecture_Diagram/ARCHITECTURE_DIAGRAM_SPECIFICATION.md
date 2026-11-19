# System Architecture Specification

**Course:** 25ITT33 - Software Engineering (Unit 3: Architectural Design & Styles)  
**System:** Retail Store Inventory and Sales Analysis System  

---

## 1. Architectural Style: 4-Tier Layered Architecture

The Retail Store Inventory and Sales Analysis System is structured using the **Layered Architectural Style** supplemented with the **Data Access Object (DAO)** pattern. This ensures loose coupling, high cohesion, clear separation of concerns, and robust testability.

```mermaid
graph TD
    subgraph Tier_1 ["Tier 1: Presentation Layer"]
        CLI["Java Interactive Console Dashboard<br>(RetailStoreApp)"]
        DEMO["Automated Demo Runner<br>(AutomatedDemoRunner)"]
        PY_CLI["Python Analytics & Visualization CLI<br>(run_full_analysis.py)"]
    end

    subgraph Tier_2 ["Tier 2: Business Logic & Application Service Layer"]
        SS["SalesService<br>• Stock pre-check<br>• Checkout orchestration<br>• Transaction boundaries"]
        IS["InventoryService<br>• Low stock identification<br>• Stock restocking<br>• Reorder calculations"]
        RS["ReportService<br>• Java 8+ Stream API<br>• Daily sales metrics<br>• Performance aggregation"]
        EX["Custom Exception Handler<br>• InsufficientStockException<br>• ProductNotFoundException"]
    end

    subgraph Tier_3 ["Tier 3: Data Access & Persistence Layer (DAO)"]
        C_DAO["CategoryDAO"]
        P_DAO["ProductDAO"]
        K_DAO["CustomerDAO"]
        I_DAO["InventoryDAO"]
        S_DAO["SalesDAO"]
        DB_CONN["DBConnection Manager<br>(Singleton JDBC Driver)"]
        PY_EXTRACT["Python DB Extractor<br>(sqlite3 engine)"]
    end

    subgraph Tier_4 ["Tier 4: Relational Database Management Layer"]
        DB[(retail_store.db<br>SQLite ACID Engine)]
        subgraph DB_Artifacts ["Database Artifacts"]
            TBL["7 Normalized Tables (3NF)<br>categories, products, customers,<br>inventory, sales_transactions,<br>sales_details, stock_updates"]
            TRG["Database Triggers<br>• trg_prevent_oversale<br>• trg_deduct_stock_on_sale<br>• trg_restock_update"]
            VW["Analytical Views<br>• v_daily_sales_summary<br>• v_low_stock_alerts<br>• v_product_sales_performance"]
        end
    end

    subgraph Tier_5 ["Tier 5: Data Science & Analytics Subsystem"]
        CLEAN["Data Preprocessing<br>• Outlier detection (IQR)<br>• Missing value imputation<br>• Feature engineering"]
        EDA["Statistical EDA<br>• Central tendency<br>• Variance & Z-scores<br>• Sales velocity"]
        VIZ["Matplotlib / Seaborn Visualizer<br>• 7 High-Resolution Charts"]
    end

    %% Presentation to Business
    CLI --> SS
    CLI --> IS
    CLI --> RS
    DEMO --> SS
    DEMO --> IS
    DEMO --> RS

    %% Business to DAO
    SS --> S_DAO
    SS --> I_DAO
    SS --> P_DAO
    SS --> EX
    IS --> I_DAO
    IS --> P_DAO
    RS --> S_DAO
    RS --> I_DAO

    %% DAO to DB
    C_DAO --> DB_CONN
    P_DAO --> DB_CONN
    K_DAO --> DB_CONN
    I_DAO --> DB_CONN
    S_DAO --> DB_CONN
    DB_CONN --> DB

    %% DB Artifacts
    DB --- TBL
    DB --- TRG
    DB --- VW

    %% Python Analytics Path
    PY_CLI --> CLEAN
    CLEAN --> EDA
    EDA --> VIZ
    CLEAN --> PY_EXTRACT
    PY_EXTRACT --> DB
```

# Software Testing Documentation
## Retail Store Inventory and Sales Analysis System

**Course:** 25ITT33 - Software Engineering (Unit 4: Software Testing)  
**Standard:** IEEE Std 829-2008 for Software Test Documentation  
**System:** Retail Store Inventory and Sales Analysis System  

---

## 1. Test Strategy and Objectives

The testing program verifies and validates all functional requirements (FR-01 to FR-06) across the three implementation tiers (DBMS, Java, and Python Data Science).

### 1.1 Types of Testing Conducted
1. **Unit Testing:** Individual verification of DAO methods, service algorithms, SQL constraints, and Python wrangling functions.
2. **Integration Testing:** Verification of data exchange across Java JDBC, SQLite database triggers, and Python SQL connectors.
3. **Black Box Testing:**
   - **Equivalence Partitioning (EP):** Dividing order quantities into valid partitions ($1 \le Q \le \text{AvailableStock}$) and invalid partitions ($Q \le 0$ or $Q > \text{AvailableStock}$).
   - **Boundary Value Analysis (BVA):** Testing boundary thresholds: exactly $0$, $1$, $\text{AvailableStock} - 1$, $\text{AvailableStock}$, and $\text{AvailableStock} + 1$.
4. **White Box Testing:**
   - **Control Flow Graph & Cyclomatic Complexity ($V(G)$):** Analyzing the stock verification logic branch in `SalesService.processSale()`.
   - **Basis Path Testing:** Deriving independent execution paths to guarantee 100% statement and branch coverage.
5. **System & Validation Testing:** End-to-end execution of sales, automatic inventory reduction, low stock alerting, and reporting.

---

## 2. White Box Testing: Cyclomatic Complexity Analysis

### 2.1 Checkout & Stock Validation Method Logic
```java
public boolean processSale(int customerId, int productId, int requestedQty) throws InsufficientStockException {
    // Node 1: Entry
    if (requestedQty <= 0) { // Node 2: Decision 1
        throw new IllegalArgumentException("Quantity must be positive"); // Node 3: Exit 1
    }
    // Node 4
    int availableStock = inventoryDAO.getAvailableStock(productId);
    if (requestedQty > availableStock) { // Node 5: Decision 2
        throw new InsufficientStockException("Insufficient stock", productId, availableStock, requestedQty); // Node 6: Exit 2
    }
    // Node 7
    boolean txSuccess = salesDAO.recordSale(customerId, productId, requestedQty);
    if (!txSuccess) { // Node 8: Decision 3
        throw new DatabaseOperationException("Transaction failed"); // Node 9: Exit 3
    }
    // Node 10: Successful commit
    return true; // Node 11: Exit 4
}
```

### 2.2 Cyclomatic Complexity Formula
Using McCabe's Cyclomatic Complexity:
$$V(G) = P + 1$$
Where $P$ is the number of predicate/decision nodes.
- Predicate Nodes: Node 2 (`requestedQty <= 0`), Node 5 (`requestedQty > availableStock`), Node 8 (`!txSuccess`).
- Number of Predicates $P = 3$.
- $$V(G) = 3 + 1 = 4$$

**Four Basis Paths to Test:**
- **Path 1:** $1 \to 2 \to 3$ (Invalid negative or zero quantity $\to$ Exception).
- **Path 2:** $1 \to 2 \to 4 \to 5 \to 6$ (Over-sale attempt: Requested > Available $\to$ InsufficientStockException).
- **Path 3:** $1 \to 2 \to 4 \to 5 \to 7 \to 8 \to 9$ (Database write failure $\to$ Rollback).
- **Path 4:** $1 \to 2 \to 4 \to 5 \to 7 \to 8 \to 10 \to 11$ (Happy path: Valid sale $\to$ Stock deducted $\to$ Success).

---

## 3. Black Box Testing: Boundary Value Analysis (BVA)

For a product with current `available_stock = 10`:
| Test Input ($Q$) | Classification | Expected Behavior | Actual Behavior | Status |
| :---: | :---: | :--- | :--- | :---: |
| **-1** | Invalid (Below Min) | Throws `IllegalArgumentException` | Rejected with validation message | **PASS** |
| **0** | Invalid (Zero) | Throws `IllegalArgumentException` | Rejected with validation message | **PASS** |
| **1** | Valid (Min Boundary) | Sale accepted; Stock becomes $9$ | Sale recorded; Stock decremented to 9 | **PASS** |
| **9** | Valid (Nominal High) | Sale accepted; Stock becomes $1$ | Sale recorded; Stock decremented to 1 | **PASS** |
| **10** | Valid (Max Available) | Sale accepted; Stock becomes $0$ | Sale recorded; Stock decremented to 0 | **PASS** |
| **11** | Invalid (Over-Sale) | Throws `InsufficientStockException` | Rejected; Stock unchanged at 10 | **PASS** |

---

## 4. Comprehensive Test Case Suite

| Test Case ID | Test Scenario | Test Input / Action | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **TC-01** | Database Schema Creation | Run `01_schema_ddl.sql` | 7 tables created with constraints | All tables & constraints verified | **PASS** |
| **TC-02** | Product Registration | Add "Wireless Mouse", Price 29.99, Stock 50 | Record inserted in `products` & `inventory` | Record inserted with PK | **PASS** |
| **TC-03** | Valid Sales Processing | Sell 5 units of Product ID 1 (Stock = 50) | Sale recorded, stock becomes 45 | Stock decremented to 45; audit logged | **PASS** |
| **TC-04** | Over-Sale Prevention (Java) | Attempt to sell 60 units (Stock = 45) | App rejects with `InsufficientStockException` | Exception thrown; transaction aborted | **PASS** |
| **TC-05** | Over-Sale Prevention (Trigger) | Direct SQL insert of 100 units in `sales_details` | Trigger `trg_prevent_oversale` aborts | Trigger raised error: "Insufficient stock" | **PASS** |
| **TC-06** | Automatic Stock Update | Sell 10 units of Product ID 2 | Stock decrements by 10 automatically | Stock reduced by 10 via DB trigger | **PASS** |
| **TC-07** | Stock Audit Logging | Inspect `stock_updates` table after sale | Audit row inserted with type 'SALE' | Audit row present with correct balance | **PASS** |
| **TC-08** | Product Restock | Restock 20 units for Product ID 1 | Stock increases from 45 to 65 | Stock updated; restock audit logged | **PASS** |
| **TC-09** | Daily Sales Report | Call `ReportService.getDailySalesSummary()` | Aggregates daily orders and total revenue | Correct totals matching DB records | **PASS** |
| **TC-10** | Low-Stock Items Query | Query products with `stock <= reorder_level` | Returns only items breaching threshold | Low-stock items correctly flagged | **PASS** |
| **TC-11** | Python DB Extraction | Run `db_extractor.py` | Extracts tables to Pandas DataFrames | 100% records loaded without data loss | **PASS** |
| **TC-12** | Python Data Preprocessing | Handle nulls, type conversions, IQR outliers | Cleaned dataframes saved to CSV | Cleaned CSV files generated | **PASS** |
| **TC-13** | Fast-Selling Products Identification | Compute sales volume per product | Top 5 best sellers ranked accurately | Output matches SQL aggregation | **PASS** |
| **TC-14** | Visualization Suite Generation | Run `visualizer.py` | 7 high-res PNG charts generated | 7 PNG image files created | **PASS** |
| **TC-15** | Automated End-to-End BAT Run | Double click runnable BAT files | Batch files execute sequentially without errors | All 3 BAT files execute smoothly | **PASS** |

---

## 5. Requirements Traceability Matrix (RTM)

| Requirement ID | Requirement Description | Class / Module | Test Case ID | Test Result |
| :---: | :--- | :--- | :---: | :---: |
| **FR-01** | Maintain Product Details | `ProductDAO.java`, `products` table | TC-01, TC-02 | **PASS** |
| **FR-02** | Record Sales Transactions | `SalesService.java`, `SalesDAO.java` | TC-03, TC-09 | **PASS** |
| **FR-03** | Auto-update Stock Quantities | `trg_deduct_stock_on_sale`, `InventoryDAO` | TC-06, TC-07 | **PASS** |
| **FR-04** | Prevent Sales Exceeding Stock | `InsufficientStockException`, `trg_prevent_oversale` | TC-04, TC-05 | **PASS** |
| **FR-05** | Daily Sales & Low Stock Reports | `ReportService.java`, Views `v_daily_sales_summary`, `v_low_stock_alerts` | TC-08, TC-10 | **PASS** |
| **FR-06** | Python Preprocessing & Visualizations | `data_preprocessor.py`, `visualizer.py` | TC-11, TC-12, TC-13, TC-14 | **PASS** |

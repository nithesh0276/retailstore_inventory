# Sequence Diagram Specification: Sales Processing Interaction

**Course:** 25ITT33 - Software Engineering (Unit 3: Software Design - Interaction Modeling)  
**System:** Retail Store Inventory and Sales Analysis System  

---

## 1. Object Interaction Overview

This sequence diagram illustrates the chronological message exchange between system components during a sales transaction, highlighting:
1. User input capture by `RetailStoreApp` (Presentation Layer).
2. Stock verification request sent to `SalesService` (Business Layer).
3. Querying on-hand stock from `InventoryDAO` and relational database.
4. Exception throwing upon stock shortfall.
5. Transactional persistence across `SalesDAO` and database triggers upon valid checkout.

---

## 2. Sequence Diagram (Mermaid)

```mermaid
sequenceDiagram
    autonumber
    actor Cashier as Cashier / Sales Clerk
    participant UI as RetailStoreApp (UI)
    participant SS as SalesService
    participant IDAO as InventoryDAO
    participant SDAO as SalesDAO
    participant DB as SQLite Database
    participant TRG as DB Triggers (Engine)

    Cashier->>UI: Enter Transaction (CustomerId, ProductId, Qty, PaymentMode)
    UI->>SS: processSale(customerId, productId, qty, paymentMode)
    
    activate SS
    SS->>IDAO: getAvailableStock(productId)
    activate IDAO
    IDAO->>DB: SELECT available_stock FROM inventory WHERE product_id = ?
    activate DB
    DB-->>IDAO: available_stock (e.g., 5 units)
    deactivate DB
    IDAO-->>SS: return available_stock
    deactivate IDAO

    alt Requested Qty > Available Stock (e.g., Qty = 10)
        SS-->>UI: throw InsufficientStockException("Only 5 units available!")
        UI-->>Cashier: Display Error: "Sale Rejected: Requested quantity exceeds stock!"
    else Requested Qty <= Available Stock (e.g., Qty = 3)
        SS->>SDAO: recordTransactionWithDetails(customerId, productId, qty, unitPrice, mode)
        activate SDAO
        SDAO->>DB: BEGIN TRANSACTION
        SDAO->>DB: INSERT INTO sales_transactions (...)
        SDAO->>DB: INSERT INTO sales_details (...)
        activate DB
        DB->>TRG: Fire BEFORE INSERT trg_prevent_oversale
        TRG-->>DB: Validation Passed
        DB->>TRG: Fire AFTER INSERT trg_deduct_stock_on_sale
        TRG->>DB: UPDATE inventory SET available_stock = available_stock - qty
        TRG->>DB: INSERT INTO stock_updates (audit log)
        deactivate DB
        SDAO->>DB: COMMIT TRANSACTION
        SDAO-->>SS: return transactionId (Success)
        deactivate SDAO
        SS-->>UI: return SaleReceiptDTO
        UI-->>Cashier: Print Invoice Receipt & Confirmation Message
    end
    deactivate SS
```

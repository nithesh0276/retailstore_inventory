# Class Diagram Specification and Design

**Course:** 25ITT33 - Software Engineering (Unit 2: Class Based Modeling & Unit 3: Software Design)  
**System:** Retail Store Inventory and Sales Analysis System  

---

## 1. Class Structure and Relationships

The system employs an Object-Oriented design adhering to the Model-View-Controller (MVC) and Data Access Object (DAO) architecture:

1. **Domain Entities (Model Layer):**
   - `Category`: Represents product classifications.
   - `Product`: Stores product identity, pricing, and links to categories.
   - `Customer`: Holds customer demographic and contact data.
   - `Inventory`: Encapsulates real-time on-hand stock and reorder thresholds.
   - `SalesTransaction`: Encapsulates master sale invoices (Customer, Date, Payment Mode, Total).
   - `SalesDetail`: Represents individual line items in a transaction (Product, Qty, Unit Price, Subtotal).
   - `StockUpdate`: Records an immutable ledger audit trail for every inventory change.

2. **Data Access Layer (DAO Layer):**
   - `CategoryDAO`, `ProductDAO`, `CustomerDAO`, `InventoryDAO`, `SalesDAO`.
   - Manages CRUD SQL operations using parameterized `PreparedStatement`.

3. **Business Logic & Service Layer:**
   - `SalesService`: Validates stock before checkout, controls ACID boundaries, coordinates line item recording, triggers stock reduction.
   - `InventoryService`: Manages restocking, stock level assertions, discrepancy audits.
   - `ReportService`: Uses Java Stream API to filter and aggregate daily sales and low-stock alerts.

4. **Exception Hierarchy:**
   - `InsufficientStockException`: Custom checked exception thrown when requested quantity > available stock.
   - `ProductNotFoundException`: Thrown when querying a non-existent product ID.

---

## 2. UML Class Diagram (Mermaid)

```mermaid
classDiagram
    class Category {
        -int categoryId
        -String categoryName
        -String description
        +getCategoryId() int
        +getCategoryName() String
        +getDescription() String
    }

    class Product {
        -int productId
        -String productName
        -int categoryId
        -double unitPrice
        -double costPrice
        -int reorderLevel
        +getProductId() int
        +getProductName() String
        +getUnitPrice() double
        +getReorderLevel() int
    }

    class Customer {
        -int customerId
        -String customerName
        -String phone
        -String email
        -String address
        +getCustomerId() int
        +getCustomerName() String
        +getPhone() String
    }

    class Inventory {
        -int inventoryId
        -int productId
        -int availableStock
        -String lastUpdated
        +getAvailableStock() int
        +deductStock(int qty) void
        +addStock(int qty) void
        +isLowStock(int reorderLevel) boolean
    }

    class SalesTransaction {
        -int transactionId
        -int customerId
        -String transactionDate
        -double totalAmount
        -String paymentMode
        -String cashierName
        -List~SalesDetail~ items
        +addItem(SalesDetail item) void
        +calculateTotal() double
    }

    class SalesDetail {
        -int detailId
        -int transactionId
        -int productId
        -int quantitySold
        -double unitPrice
        -double subtotal
        +getSubtotal() double
        +getQuantitySold() int
    }

    class StockUpdate {
        -int updateId
        -int productId
        -int changeQuantity
        -String updateType
        -int balanceStock
        -String timestamp
        -String notes
    }

    class SalesService {
        -SalesDAO salesDAO
        -InventoryDAO inventoryDAO
        -ProductDAO productDAO
        +processSale(SalesTransaction tx) boolean
        +validateStock(int productId, int requestedQty) boolean
    }

    class InventoryService {
        -InventoryDAO inventoryDAO
        +checkStock(int productId) int
        +restockProduct(int productId, int qty) boolean
        +getLowStockItems() List~Product~
    }

    class InsufficientStockException {
        -int productId
        -int availableQty
        -int requestedQty
        +getMessage() String
    }

    Category "1" -- "0..*" Product : classifies
    Product "1" -- "1" Inventory : has stock
    Customer "1" -- "0..*" SalesTransaction : places
    SalesTransaction "1" *-- "1..*" SalesDetail : contains
    Product "1" -- "0..*" SalesDetail : ordered in
    Product "1" -- "0..*" StockUpdate : audited in
    SalesService ..> InsufficientStockException : throws
    SalesService ..> SalesTransaction : orchestrates
    InventoryService ..> Inventory : manages
```

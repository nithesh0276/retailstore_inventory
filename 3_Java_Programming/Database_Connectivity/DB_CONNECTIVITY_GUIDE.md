# Java Database Connectivity (JDBC) Guide

**Course:** 25ITT32 - Java Programming (Unit 4: String Handling and Database Connection)  
**Database Driver:** `org.sqlite.JDBC` (`sqlite-jdbc-3.45.2.0.jar`)  
**Database URL:** `jdbc:sqlite:retail_store.db`  

---

## 1. Overview of JDBC Architecture in the System

The Java application integrates directly with the embedded SQLite ACID database (`retail_store.db`) using the official **Xerial SQLite JDBC Driver**. 

```
[ Java Service Layer ]
          ↓ Calls
[ Data Access Objects (DAOs) ]
          ↓ Creates PreparedStatements
[ DBConnection (Singleton Connection Manager) ]
          ↓ Interfaces via JDBC Driver
[ org.sqlite.JDBC Driver (`lib/sqlite-jdbc.jar`) ]
          ↓ Reads & Writes
[ Embedded SQLite Database (`retail_store.db`) ]
```

---

## 2. Key JDBC Implementation Features

### 2.1 Connection Management (`DBConnection.java`)
- Implements the **Singleton Pattern** to guarantee a single reusable database connection per thread/session.
- Enforces SQLite foreign key constraints dynamically:
  ```java
  Class.forName("org.sqlite.JDBC");
  connection = DriverManager.getConnection("jdbc:sqlite:retail_store.db");
  connection.createStatement().execute("PRAGMA foreign_keys = ON;");
  ```
- Features a dynamic path resolver that locates `retail_store.db` regardless of whether the application is launched from IDE, console root, or subfolder.

### 2.2 SQL Injection Prevention via `PreparedStatement`
All dynamic queries use parameterized `PreparedStatement` to ensure 100% immunity against SQL injection attacks:
```java
String sql = "SELECT available_stock FROM inventory WHERE product_id = ?;";
PreparedStatement pstmt = conn.prepareStatement(sql);
pstmt.setInt(1, productId);
ResultSet rs = pstmt.executeQuery();
```

### 2.3 ACID Transaction Boundaries in Java
Multi-table inserts (Sales Transaction + Line Items) enforce strict Atomicity:
```java
conn.setAutoCommit(false); // Begin transaction
try {
    // 1. Insert master transaction
    // 2. Insert line items
    conn.commit(); // Commit all modifications
} catch (SQLException e) {
    conn.rollback(); // Rollback on any failure
    throw new DatabaseOperationException("Transaction aborted: " + e.getMessage(), e);
} finally {
    conn.setAutoCommit(true);
}
```

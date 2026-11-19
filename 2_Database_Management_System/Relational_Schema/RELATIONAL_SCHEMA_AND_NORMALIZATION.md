# Relational Schema Design and Normalization Analysis

**Course:** 25ITT31 - Database Management Systems (Unit 1: Relational Model & Unit 3: Normalization)  
**System:** Retail Store Inventory and Sales Analysis System  

---

## 1. Formal Relational Schema Mapping

The conceptual E-R model is mapped to seven relational tables with primary keys ($\underline{\text{underlined}}$) and foreign keys ($\text{italicized}$):

1. **`categories`** ($\underline{\text{category\_id}}$, category\_name, description)
2. **`products`** ($\underline{\text{product\_id}}$, product\_name, $\text{category\_id}$, unit\_price, cost\_price, reorder\_level)
   - $\text{category\_id} \to \text{categories}(\text{category\_id})$
3. **`customers`** ($\underline{\text{customer\_id}}$, customer\_name, phone, email, address)
4. **`inventory`** ($\underline{\text{inventory\_id}}$, $\text{product\_id}$, available\_stock, last\_updated)
   - $\text{product\_id} \to \text{products}(\text{product\_id})$
5. **`sales_transactions`** ($\underline{\text{transaction\_id}}$, $\text{customer\_id}$, transaction\_date, total\_amount, payment\_mode, cashier\_name)
   - $\text{customer\_id} \to \text{customers}(\text{customer\_id})$
6. **`sales_details`** ($\underline{\text{detail\_id}}$, $\text{transaction\_id}$, $\text{product\_id}$, quantity\_sold, unit\_price, subtotal)
   - $\text{transaction\_id} \to \text{sales_transactions}(\text{transaction\_id})$
   - $\text{product\_id} \to \text{products}(\text{product\_id})$
7. **`stock_updates`** ($\underline{\text{update\_id}}$, $\text{product\_id}$, change\_quantity, update\_type, balance\_stock, update\_timestamp, notes)
   - $\text{product\_id} \to \text{products}(\text{product\_id})$

---

## 2. Functional Dependencies (FDs) Analysis

Let the set of functional dependencies for each relation be:

### 2.1 Relation: `categories`
- $FD_1: \text{category\_id} \to \{\text{category\_name}, \text{description}\}$
- $FD_2: \text{category\_name} \to \{\text{category\_id}, \text{description}\}$ (Candidate Key)
- Candidate Keys: $\{\text{category\_id}\}, \{\text{category\_name}\}$.

### 2.2 Relation: `products`
- $FD_3: \text{product\_id} \to \{\text{product\_name}, \text{category\_id}, \text{unit\_price}, \text{cost\_price}, \text{reorder\_level}\}$
- Candidate Key: $\{\text{product\_id}\}$.

### 2.3 Relation: `customers`
- $FD_4: \text{customer\_id} \to \{\text{customer\_name}, \text{phone}, \text{email}, \text{address}\}$
- $FD_5: \text{phone} \to \{\text{customer\_id}, \text{customer\_name}, \text{email}, \text{address}\}$ (Unique Contact Key)
- Candidate Keys: $\{\text{customer\_id}\}, \{\text{phone}\}$.

### 2.4 Relation: `inventory`
- $FD_6: \text{inventory\_id} \to \{\text{product\_id}, \text{available\_stock}, \text{last\_updated}\}$
- $FD_7: \text{product\_id} \to \{\text{inventory\_id}, \text{available\_stock}, \text{last\_updated}\}$ (1:1 with Product)
- Candidate Keys: $\{\text{inventory\_id}\}, \{\text{product\_id}\}$.

### 2.5 Relation: `sales_transactions`
- $FD_8: \text{transaction\_id} \to \{\text{customer\_id}, \text{transaction\_date}, \text{total\_amount}, \text{payment\_mode}, \text{cashier\_name}\}$
- Candidate Key: $\{\text{transaction\_id}\}$.

### 2.6 Relation: `sales_details`
- $FD_9: \text{detail\_id} \to \{\text{transaction\_id}, \text{product\_id}, \text{quantity\_sold}, \text{unit\_price}, \text{subtotal}\}$
- $FD_{10}: \{\text{transaction\_id}, \text{product\_id}\} \to \{\text{detail\_id}, \text{quantity\_sold}, \text{unit\_price}, \text{subtotal}\}$
- Candidate Keys: $\{\text{detail\_id}\}, \{\text{transaction\_id}, \text{product\_id}\}$.

### 2.7 Relation: `stock_updates`
- $FD_{11}: \text{update\_id} \to \{\text{product\_id}, \text{change\_quantity}, \text{update\_type}, \text{balance\_stock}, \text{update\_timestamp}, \text{notes}\}$
- Candidate Key: $\{\text{update\_id}\}$.

---

## 3. Formal Normalization Proofs (1NF to BCNF)

### 3.1 First Normal Form (1NF)
- **Criterion:** All attributes contain only atomic (indivisible) values, and there are no repeating groups or multivalued columns.
- **Verification:** In all relations, phone numbers, addresses, names, quantities, and prices are singular, atomic scalar values. No comma-delimited lists or nested tables exist. Hence, all relations satisfy **1NF**.

### 3.2 Second Normal Form (2NF)
- **Criterion:** The relation must be in 1NF, and no non-prime attribute may be partially functionally dependent on any candidate key (full functional dependency).
- **Verification:**
  - For tables with single-attribute primary keys (`categories`, `products`, `customers`, `inventory`, `sales_transactions`, `stock_updates`), partial key dependency is mathematically impossible.
  - In `sales_details`, the composite key is $\{\text{transaction\_id}, \text{product\_id}\}$. The attribute `unit_price` recorded here is the *historical transaction unit price* (not current catalog price), which depends on both transaction and product. `quantity_sold` and `subtotal` also depend fully on the composite key.
  - Hence, no partial dependencies exist. All relations satisfy **2NF**.

### 3.3 Third Normal Form (3NF)
- **Criterion:** The relation must be in 2NF, and for every non-trivial functional dependency $X \to Y$, either:
  1. $X$ is a superkey, or
  2. $Y$ is a prime attribute (member of a candidate key).
- **Verification:**
  - In `products`, category details (`category_name`, `description`) are not stored; only `category_id` FK is stored. Thus, transitive dependency $\text{product\_id} \to \text{category\_id} \to \text{category\_name}$ is eliminated.
  - In `sales_transactions`, customer address/phone is not stored; only `customer_id` FK is stored.
  - In every functional dependency $X \to Y$, $X$ is a candidate key.
  - Hence, all relations satisfy **3NF**.

### 3.4 Boyce-Codd Normal Form (BCNF)
- **Criterion:** For every non-trivial functional dependency $X \to Y$, $X$ must be a strict superkey.
- **Verification:**
  - In all relations, every determinant ($X$) in each functional dependency $X \to Y$ is a valid superkey.
  - No anomalies (Insertion, Update, Deletion) can occur.
  - Therefore, the database schema strictly satisfies **BCNF**.

# Data Preprocessing and Transformation Documentation

**Course:** 25ITC31 - Foundations of Data Science (Unit 4: Data Cleaning and Transformation Techniques)  
**System:** Retail Store Inventory and Sales Analysis System  

---

## 1. Objectives of Data Preprocessing
The operational SQLite database records raw point-of-sale transactions and inventory levels. Before statistical analysis and visualization, the raw records must undergo systematic cleaning and transformation to ensure high data quality:
1. Handling missing values and ensuring referential completeness.
2. Detecting and eliminating duplicate transactional records.
3. Converting string and numeric data types into native NumPy/Pandas formats (Datetime, float64, int64).
4. Detecting and interpreting transactional outliers using the Interquartile Range (IQR) technique.
5. Deriving new domain-specific features (Revenue, Gross Profit, Margin %, Inventory Valuation, Reorder Deficit, Stock Urgency Category).

---

## 2. Preprocessing Steps Implemented in `data_preprocessor.py`

### 2.1 Missing Value and Duplicate Treatment
- **Duplicate Verification:** Checked primary keys (`product_id` and `detail_id`). Duplicate count = 0 across all tables.
- **Null Handling:** `available_stock` and `reorder_level` were checked for null values. Any unlinked inventory defaults cleanly to 0, ensuring no NaN values propagate into downstream computations.

### 2.2 Data Type Casting
- Transaction timestamps parsed to `pandas.DatetimeIndex`.
- Extracted calendar `sale_date` (YYYY-MM-DD) and categorical `day_of_week` (Monday–Sunday) for cyclical sales trend evaluation.
- Cast `unit_price`, `cost_price`, and `subtotal` to double-precision floats (`float64`).

### 2.3 Outlier Detection using Interquartile Range (IQR)
Under Tukey's boxplot method:
$$\text{IQR} = Q_3 - Q_1$$
$$\text{Lower Bound} = \max(0, Q_1 - 1.5 \times \text{IQR})$$
$$\text{Upper Bound} = Q_3 + 1.5 \times \text{IQR}$$
- For order line amounts (`subtotal`), transactions exceeding the upper bound represent high-value bulk purchases (e.g. premium electronics like headphones or bulk staples). These are flagged and preserved as valid legitimate business spikes rather than sensor corruptions.

### 2.4 Feature Engineering
1. **Gross Profit:**
   $$\text{Gross Profit} = \text{Quantity Sold} \times (\text{Unit Price} - \text{Cost Price})$$
2. **Gross Profit Margin Percentage:**
   $$\text{Profit Margin \%} = \left(\frac{\text{Gross Profit}}{\text{Subtotal}}\right) \times 100$$
3. **Inventory Asset Valuation:**
   $$\text{Inventory Valuation} = \text{Available Stock} \times \text{Unit Selling Price}$$
4. **Stock Urgency Status:** Categorical classification based on safety thresholds:
   - `OUT_OF_STOCK`: $\text{Available Stock} = 0$
   - `CRITICAL`: $0 < \text{Available Stock} \le \frac{\text{Reorder Level}}{2}$
   - `LOW_STOCK`: $\frac{\text{Reorder Level}}{2} < \text{Available Stock} \le \text{Reorder Level}$
   - `ADEQUATE`: $\text{Available Stock} > \text{Reorder Level}$

---

## 3. Cleaned Dataset Artifacts Exported

The pipeline generates three clean CSV files in `Data_Preprocessing/`:
- `cleaned_products.csv`: Catalog with calculated inventory valuation and stock health statuses.
- `cleaned_sales.csv`: Enriched transactional dataset with dates, day of week, profits, and margins.
- `inventory_status.csv`: Focused operational snapshot for supply chain restocking.

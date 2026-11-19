# Statistical Data Analysis and Business Intelligence Report

**Course:** 25ITC31 - Foundations of Data Science (Unit 1: Data Description & Unit 3: Data Wrangling)  
**System:** Retail Store Inventory and Sales Analysis System  

---

## 1. Executive Summary

This report presents empirical findings from statistical modeling, exploratory data analysis (EDA), and inventory risk assessments conducted on operational data extracted from the Retail Store Inventory and Sales Analysis System.

---

## 2. Descriptive Statistics of Transactional Values

Measures of central tendency and dispersion computed on order line item amounts (`subtotal`):

| Statistical Metric | Symbol / Formula | Empirical Value | Business Interpretation |
| :--- | :---: | :---: | :--- |
| **Sample Size ($N$)** | $N$ | 31 Line Items | Total itemized purchase records analyzed |
| **Mean Line Value** | $\bar{X} = \frac{\sum X}{N}$ | **\$34.26** | Average spending per line item across catalog |
| **Median Line Value** | $\tilde{X}$ ($50^{\text{th}}$ percentile) | **\$24.99** | Central transaction amount; resistant to extreme outliers |
| **Standard Deviation** | $\sigma$ | **\$30.73** | Substantial dispersion reflecting mix of low-cost grocery items and premium electronics |
| **Variance** | $\sigma^2$ | **\$944.33** | Total spread of squared deviations |
| **Minimum Value** | $X_{\min}$ | **\$4.25** | Smallest line sale (Single unit of Natural Coconut Water) |
| **Maximum Value** | $X_{\max}$ | **\$129.99** | Largest single line sale (Noise Cancelling Headphones) |
| **First Quartile ($Q_1$)** | $25^{\text{th}}$ percentile | **\$14.25** | 25% of purchases are below \$14.25 |
| **Third Quartile ($Q_3$)** | $75^{\text{th}}$ percentile | **\$44.98** | 75% of purchases are below \$44.98 |
| **Interquartile Range** | $\text{IQR} = Q_3 - Q_1$ | **\$30.73** | Middle 50% spread of transaction line values |

---

## 3. Category-Wise Sales and Financial Performance

| Category Name | Total Catalog SKUs | Units Sold | Total Revenue ($) | Gross Profit ($) | Gross Margin (%) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Electronics** | 4 | 22 | **\$644.78** | \$283.40 | 43.95% |
| **Groceries & Staples** | 4 | 8 | **\$134.48** | \$37.60 | 27.96% |
| **Home & Kitchen** | 4 | 8 | **\$131.45** | \$57.90 | 44.05% |
| **Beverages & Snacks** | 4 | 11 | **\$112.41** | \$44.40 | 39.50% |
| **Personal Care** | 4 | 6 | **\$45.47** | \$21.20 | 46.62% |
| **Total / Store Average** | **20** | **55** | **\$1,068.59** | **\$444.50** | **41.60%** |

**Key Insights:**
- **Revenue Driver:** The **Electronics** category drives the highest revenue (\$644.78, representing over 60% of total revenue) due to high unit values and high demand for peripherals.
- **Highest Margin Category:** **Personal Care** yields the highest gross margin percentage (46.62%), followed closely by **Electronics** (43.95%) and **Home & Kitchen** (44.05%).

---

## 4. Fast-Selling Products Identification (Top 5 Ranking)

1. **USB-C Fast Charging Cable (Electronics):** 10 units sold | \$129.90 Revenue | 80 units remaining.
2. **Wireless Optical Mouse (Electronics):** 9 units sold | \$224.91 Revenue | 56 units remaining.
3. **Mechanical Gaming Keyboard (Electronics):** 4 units sold | \$319.96 Revenue | 36 units remaining.
4. **Basmati Rice Premium (5kg) (Groceries):** 4 units sold | \$74.00 Revenue | 71 units remaining.
5. **Arabica Dark Roast Coffee Beans (Beverages):** 4 units sold | \$67.96 Revenue | 31 units remaining.

---

## 5. Low-Stock & Supply Chain Risk Assessment

Products currently breaching safety reorder thresholds:
1. **Non-Stick Ceramic Frying Pan (28cm):** Available Stock = 3 units | Reorder Level = 8 | **Deficit = -5 units (CRITICAL)**.
2. **Natural Coconut Water (1L):** Available Stock = 6 units | Reorder Level = 30 | **Deficit = -24 units (CRITICAL)**.

**Supply Chain Recommendation:**
Trigger immediate purchase orders for Non-Stick Ceramic Frying Pan (+13 units) and Natural Coconut Water (+54 units) to restore safety buffers and prevent stockouts.

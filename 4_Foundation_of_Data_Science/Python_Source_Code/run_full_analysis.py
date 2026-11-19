import os
import sys

# Ensure current dir is in path
sys.path.append(os.path.dirname(__file__))

from db_extractor import extract_raw_datasets
from data_preprocessor import clean_and_transform
from data_analyzer import perform_statistical_analysis
from visualizer import generate_all_visualizations

"""
Master Execution Pipeline for Foundation of Data Science.
Academic Regulation: VCET B.Tech IT (R2025) | Course: 25ITC31
Register No: 9, 39, 69, 99
"""

def execute_complete_pipeline():
    base_fds = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    out_dir = os.path.join(base_fds, "Output")
    viz_dir = os.path.join(base_fds, "Visualizations")
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(viz_dir, exist_ok=True)
    output_txt_path = os.path.join(out_dir, "data_science_analysis_output.txt")

    log = []
    
    def log_print(msg=""):
        print(msg)
        log.append(msg)

    log_print("=" * 90)
    log_print("   FOUNDATION OF DATA SCIENCE - RETAIL SALES & INVENTORY ANALYTICS PIPELINE")
    log_print("   Academic Regulation: VCET B.Tech IT (R2025) | Course Code: 25ITC31")
    log_print("   Register Numbers: 9, 39, 69, 99")
    log_print("=" * 90)

    # 1. Extraction
    log_print("\n[PHASE 1] DATA RETRIEVAL & EXTRACTION (sqlite3 Engine)")
    log_print("-" * 75)
    df_products, df_sales, df_categories, df_audits = extract_raw_datasets()
    log_print(f"  • Extracted Products Dataset     : {len(df_products)} rows, {df_products.shape[1]} features")
    log_print(f"  • Extracted Sales Items Dataset  : {len(df_sales)} rows, {df_sales.shape[1]} features")
    log_print(f"  • Extracted Categories           : {len(df_categories)} classifications")
    log_print(f"  • Extracted Audit Logs           : {len(df_audits)} inventory movement records")

    # 2. Preprocessing
    log_print("\n[PHASE 2] DATA CLEANING & FEATURE ENGINEERING (Unit 4: Preprocessing)")
    log_print("-" * 75)
    df_prod_clean, df_sales_clean = clean_and_transform(df_products, df_sales)
    log_print(f"  • Missing Values Handled        : Imputed zero for unlinked stock, 10 for default reorder")
    log_print(f"  • Date Casting & Extraction     : Formatted timestamps to DatetimeIndex, extracted Day of Week")
    log_print(f"  • New Engineered Features       : gross_profit, profit_margin_pct, inventory_valuation, stock_status")
    log_print(f"  • Cleaned Datasets Exported     : Data_Preprocessing/cleaned_products.csv, cleaned_sales.csv")

    # 3. Statistical Analysis
    log_print("\n[PHASE 3] EXPLORATORY DATA ANALYSIS & DESCRIPTIVE STATISTICS (Unit 1 & 3)")
    log_print("-" * 75)
    res = perform_statistical_analysis(df_prod_clean, df_sales_clean)

    so = res['sales_overview']
    log_print(f"1. Executive Sales Overview:")
    log_print(f"   - Total Processed Orders        : {so['total_orders']} orders")
    log_print(f"   - Total Units Sold              : {so['total_units_sold']} items")
    log_print(f"   - Total Sales Revenue           : ${so['total_revenue']:,.2f}")
    log_print(f"   - Total Gross Profit            : ${so['total_gross_profit']:,.2f}")
    log_print(f"   - Overall Gross Margin          : {so['overall_profit_margin_pct']:.2f}%")
    log_print(f"   - Average Order Value (AOV)     : ${so['average_order_value']:.2f}")

    inv = res['inventory_summary']
    log_print(f"\n2. Inventory Position & Valuation:")
    log_print(f"   - Total On-Hand Stock           : {inv['total_on_hand_units']} units")
    log_print(f"   - Total Inventory Asset Value   : ${inv['total_inventory_valuation']:,.2f}")
    log_print(f"   - Low-Stock Products Count      : {inv['low_stock_item_count']} items")
    log_print(f"   - Critical Risk Items Count     : {inv['critical_stock_count']} items")

    stats = res['subtotal_descriptive_stats']
    log_print(f"\n3. Descriptive Statistics for Order Line Values (Unit 1 Measures):")
    log_print(f"   - Mean Line Value               : ${stats['mean']:.2f}")
    log_print(f"   - Median Line Value             : ${stats['median']:.2f}")
    log_print(f"   - Standard Deviation (sigma)    : ${stats['std_dev']:.2f}")
    log_print(f"   - Variance (sigma^2)            : ${stats['variance']:.2f}")
    log_print(f"   - Minimum Transaction Value     : ${stats['min']:.2f}")
    log_print(f"   - Maximum Transaction Value     : ${stats['max']:.2f}")
    log_print(f"   - Interquartile Range (IQR)     : ${stats['iqr']:.2f} (Q1=${stats['q1_25pct']:.2f}, Q3=${stats['q3_75pct']:.2f})")

    # Table 1: Category Performance Table
    log_print(f"\n4. Category-Wise Performance Summary:")
    log_print(f"{'CATEGORY NAME':<25} | {'UNITS SOLD':<11} | {'REVENUE ($)':<12} | {'GROSS PROFIT ($)':<16}")
    log_print("-" * 72)
    for _, r in res['category_performance'].iterrows():
        log_print(f"{r['category_name']:<25} | {int(r['units_sold']):<11} | {r['revenue']:<12.2f} | {r['profit']:<16.2f}")

    # Table 2: Top 5 Fast Selling
    log_print(f"\n5. Fast-Selling Products (Ranked by Sales Volume & Turnover):")
    log_print(f"{'ID':<4} | {'PRODUCT NAME':<32} | {'CATEGORY':<18} | {'UNITS':<6} | {'REVENUE ($)':<12} | {'ON-HAND':<8}")
    log_print("-" * 92)
    for _, r in res['fast_selling_products'].iterrows():
        log_print(f"{r['product_id']:<4} | {r['product_name']:<32} | {r['category_name']:<18} | {int(r['units_sold']):<6} | {r['total_revenue']:<12.2f} | {int(r['available_stock']):<8}")

    # Table 3: Low Stock Alerts
    log_print(f"\n6. Low-Stock / Critical Inventory Alert Table:")
    log_print(f"{'ID':<4} | {'PRODUCT NAME':<32} | {'CATEGORY':<18} | {'STOCK':<6} | {'REORDER':<8} | {'STATUS':<10}")
    log_print("-" * 88)
    for _, r in res['low_stock_products'].iterrows():
        log_print(f"{r['product_id']:<4} | {r['product_name']:<32} | {r['category_name']:<18} | {int(r['available_stock']):<6} | {int(r['reorder_level']):<8} | {r['stock_status']:<10}")

    # Table 4: Daily Sales Trends
    log_print(f"\n7. Daily Sales Trends Analysis:")
    log_print(f"{'DATE':<12} | {'ORDERS':<8} | {'UNITS SOLD':<11} | {'DAILY REVENUE ($)':<18} | {'PROFIT ($)':<12}")
    log_print("-" * 72)
    for _, r in res['daily_sales'].iterrows():
        log_print(f"{str(r['sale_date']):<12} | {int(r['orders']):<8} | {int(r['units_sold']):<11} | {r['daily_revenue']:<18.2f} | {r['daily_profit']:<12.2f}")

    # 4. Generate Visualizations
    log_print("\n[PHASE 4] RENDERING VISUALIZATION DASHBOARD (Unit 5: EDA & Charts)")
    log_print("-" * 75)
    generate_all_visualizations(df_prod_clean, df_sales_clean, res, viz_dir)
    log_print(f"  • Chart 1: Category Distribution (1_category_distribution.png)")
    log_print(f"  • Chart 2: Product Sales Volume vs Revenue (2_product_sales_volume_and_revenue.png)")
    log_print(f"  • Chart 3: Daily Sales Revenue Trend (3_daily_sales_trends.png)")
    log_print(f"  • Chart 4: Stock Availability vs Reorder Thresholds (4_stock_availability_vs_reorder.png)")
    log_print(f"  • Chart 5: Fast-Selling Products Ranking (5_fast_selling_products.png)")
    log_print(f"  • Chart 6: Low-Stock Risk Deficit Analysis (6_low_stock_risk_analysis.png)")
    log_print(f"  • Chart 7: Feature Correlation Matrix Heatmap (7_correlation_matrix_heatmap.png)")

    log_print("\n" + "=" * 90)
    log_print("   FOUNDATION OF DATA SCIENCE PIPELINE COMPLETED SUCCESSFULLY!")
    log_print("=" * 90)

    # Save to Output text file
    with open(output_txt_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(log))
    print(f"\n[INFO] Comprehensive Data Science output saved to: {output_txt_path}")

if __name__ == "__main__":
    execute_complete_pipeline()

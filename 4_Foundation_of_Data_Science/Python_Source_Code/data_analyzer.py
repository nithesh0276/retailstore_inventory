import pandas as pd
import numpy as np

"""
Data Analyzer Module: Statistical Modeling, Descriptive Metrics & Business Insights.
Course: 25ITC31 Foundations of Data Science (Unit 1: Data Description & Unit 3: Data Wrangling)
"""

def perform_statistical_analysis(df_products, df_sales):
    results = {}

    print("\n[ANALYZER] Computing Descriptive Statistics and Business Performance Metrics...")

    # 1. Total Catalog & Category Distribution
    total_products = len(df_products)
    cat_dist = df_products['category_name'].value_counts()
    results['total_products'] = total_products
    results['category_distribution'] = cat_dist

    # 2. Total Sales and Revenue
    total_orders = df_sales['transaction_id'].nunique()
    total_units_sold = df_sales['quantity_sold'].sum()
    total_revenue = df_sales['subtotal'].sum()
    total_gross_profit = df_sales['gross_profit'].sum()
    overall_profit_margin = (total_gross_profit / total_revenue) * 100 if total_revenue > 0 else 0
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

    results['sales_overview'] = {
        'total_orders': total_orders,
        'total_units_sold': total_units_sold,
        'total_revenue': total_revenue,
        'total_gross_profit': total_gross_profit,
        'overall_profit_margin_pct': overall_profit_margin,
        'average_order_value': avg_order_value
    }

    # 3. Descriptive Statistics for Sales Amounts (Unit 1: Central Tendency & Dispersion)
    subtotal_series = df_sales['subtotal']
    stats_subtotal = {
        'mean': subtotal_series.mean(),
        'median': subtotal_series.median(),
        'std_dev': subtotal_series.std(),
        'variance': subtotal_series.var(),
        'min': subtotal_series.min(),
        'max': subtotal_series.max(),
        'q1_25pct': subtotal_series.quantile(0.25),
        'q3_75pct': subtotal_series.quantile(0.75),
        'iqr': subtotal_series.quantile(0.75) - subtotal_series.quantile(0.25)
    }
    results['subtotal_descriptive_stats'] = stats_subtotal

    # 4. Daily Sales Analysis
    daily_sales = df_sales.groupby('sale_date').agg(
        orders=('transaction_id', 'nunique'),
        units_sold=('quantity_sold', 'sum'),
        daily_revenue=('subtotal', 'sum'),
        daily_profit=('gross_profit', 'sum')
    ).reset_index().sort_values('sale_date')
    results['daily_sales'] = daily_sales

    # 5. Fast-Selling Products (Top 5 by Units & Revenue)
    product_performance = df_sales.groupby(['product_id', 'product_name', 'category_name']).agg(
        units_sold=('quantity_sold', 'sum'),
        total_revenue=('subtotal', 'sum'),
        gross_profit=('gross_profit', 'sum')
    ).reset_index()

    # Merge current available stock
    product_performance = product_performance.merge(
        df_products[['product_id', 'available_stock', 'reorder_level']], on='product_id', how='left'
    )
    top_fast_selling = product_performance.sort_values(by=['units_sold', 'total_revenue'], ascending=[False, False]).head(5)
    results['fast_selling_products'] = top_fast_selling
    results['product_performance'] = product_performance

    # 6. Low-Stock Identification
    low_stock = df_products[df_products['available_stock'] <= df_products['reorder_level']].sort_values('available_stock')
    results['low_stock_products'] = low_stock

    # 7. Inventory Availability & Valuation
    total_on_hand_units = df_products['available_stock'].sum()
    total_inventory_valuation = df_products['inventory_valuation'].sum()
    results['inventory_summary'] = {
        'total_on_hand_units': total_on_hand_units,
        'total_inventory_valuation': total_inventory_valuation,
        'low_stock_item_count': len(low_stock),
        'critical_stock_count': len(df_products[df_products['stock_status'] == 'CRITICAL'])
    }

    # 8. Category-Wise Revenue Breakdown
    cat_performance = df_sales.groupby('category_name').agg(
        units_sold=('quantity_sold', 'sum'),
        revenue=('subtotal', 'sum'),
        profit=('gross_profit', 'sum')
    ).reset_index().sort_values('revenue', ascending=False)
    results['category_performance'] = cat_performance

    return results

if __name__ == "__main__":
    from db_extractor import extract_raw_datasets
    from data_preprocessor import clean_and_transform
    p, s, _, _ = extract_raw_datasets()
    p_clean, s_clean = clean_and_transform(p, s)
    res = perform_statistical_analysis(p_clean, s_clean)
    print("Sales Overview:", res['sales_overview'])

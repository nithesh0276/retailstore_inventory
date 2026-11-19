import os
import pandas as pd
import numpy as np

"""
Data Preprocessing Module: Cleaning, Transformation, Outlier Detection & Feature Engineering.
Course: 25ITC31 Foundations of Data Science (Unit 4: Data Cleaning and Transformation Techniques)
"""

def clean_and_transform(df_products, df_sales):
    print("\n[PREPROCESSOR] Starting Data Cleaning and Feature Engineering Pipeline...")
    
    # -------------------------------------------------------------------------
    # 1. Missing Value and Duplicate Detection
    # -------------------------------------------------------------------------
    prod_nulls = df_products.isnull().sum().to_dict()
    sales_nulls = df_sales.isnull().sum().to_dict()
    prod_dups = df_products.duplicated(subset=['product_id']).sum()
    sales_dups = df_sales.duplicated(subset=['detail_id']).sum()

    print(f"  -> Products Missing Values: {prod_nulls}")
    print(f"  -> Sales Missing Values   : {sales_nulls}")
    print(f"  -> Duplicate Records Found: Products={prod_dups}, Sales={sales_dups}")

    # Impute missing values if any
    df_products['available_stock'] = df_products['available_stock'].fillna(0).astype(int)
    df_products['reorder_level'] = df_products['reorder_level'].fillna(10).astype(int)

    # -------------------------------------------------------------------------
    # 2. Data Type Conversions (Unit 4: Type Conversion)
    # -------------------------------------------------------------------------
    df_sales['transaction_date'] = pd.to_datetime(df_sales['transaction_date'])
    df_sales['sale_date'] = df_sales['transaction_date'].dt.date
    df_sales['day_of_week'] = df_sales['transaction_date'].dt.day_name()
    df_sales['unit_price'] = df_sales['unit_price'].astype(float)
    df_sales['quantity_sold'] = df_sales['quantity_sold'].astype(int)
    df_sales['subtotal'] = df_sales['subtotal'].astype(float)

    # -------------------------------------------------------------------------
    # 3. Outlier Identification via Interquartile Range (IQR) (Unit 4)
    # -------------------------------------------------------------------------
    Q1 = df_sales['subtotal'].quantile(0.25)
    Q3 = df_sales['subtotal'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = max(0, Q1 - 1.5 * IQR)
    upper_bound = Q3 + 1.5 * IQR
    outliers = df_sales[(df_sales['subtotal'] < lower_bound) | (df_sales['subtotal'] > upper_bound)]
    print(f"  -> Outlier Detection on Line Subtotal (IQR Method):")
    print(f"     Q1=${Q1:.2f}, Q3=${Q3:.2f}, IQR=${IQR:.2f}")
    print(f"     Normal Range: [${lower_bound:.2f}, ${upper_bound:.2f}]")
    print(f"     Outlier Transactions Identified: {len(outliers)} items (e.g. premium bulk purchases)")

    # -------------------------------------------------------------------------
    # 4. Feature Creation / Feature Engineering (Unit 4)
    # -------------------------------------------------------------------------
    # Revenue, Gross Profit, and Margin in Sales
    df_sales['gross_profit'] = df_sales['quantity_sold'] * (df_sales['unit_price'] - df_sales['cost_price'])
    df_sales['profit_margin_pct'] = (df_sales['gross_profit'] / df_sales['subtotal']) * 100

    # Stock features in Products
    df_products['inventory_valuation'] = df_products['available_stock'] * df_products['unit_price']
    df_products['reorder_deficit'] = df_products['reorder_level'] - df_products['available_stock']
    df_products['stock_status'] = np.where(
        df_products['available_stock'] == 0, 'OUT_OF_STOCK',
        np.where(df_products['available_stock'] <= df_products['reorder_level'] / 2, 'CRITICAL',
        np.where(df_products['available_stock'] <= df_products['reorder_level'], 'LOW_STOCK', 'ADEQUATE'))
    )

    # -------------------------------------------------------------------------
    # 5. Export Cleaned Datasets to CSV
    # -------------------------------------------------------------------------
    out_dir = os.path.join(os.path.dirname(__file__), "..", "Data_Preprocessing")
    os.makedirs(out_dir, exist_ok=True)

    prod_csv = os.path.join(out_dir, "cleaned_products.csv")
    sales_csv = os.path.join(out_dir, "cleaned_sales.csv")
    inv_csv = os.path.join(out_dir, "inventory_status.csv")

    df_products.to_csv(prod_csv, index=False)
    df_sales.to_csv(sales_csv, index=False)
    df_products[['product_id', 'product_name', 'category_name', 'available_stock', 'reorder_level', 'stock_status', 'inventory_valuation']].to_csv(inv_csv, index=False)

    print(f"[PREPROCESSOR] Cleaned files successfully generated:")
    print(f"  -> {prod_csv}")
    print(f"  -> {sales_csv}")
    print(f"  -> {inv_csv}")

    return df_products, df_sales

if __name__ == "__main__":
    from db_extractor import extract_raw_datasets
    p, s, _, _ = extract_raw_datasets()
    clean_and_transform(p, s)

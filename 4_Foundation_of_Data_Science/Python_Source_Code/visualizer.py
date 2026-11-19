import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

os.environ['MPLCONFIGDIR'] = os.environ.get('TEMP', '.')

"""
Visualizer Module: High-Resolution Matplotlib and Seaborn Graphical Analytics.
Course: 25ITC31 Foundations of Data Science (Unit 5: EDA and Visualization Techniques)
"""

def generate_all_visualizations(df_products, df_sales, analysis_results, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({'font.sans-serif': 'DejaVu Sans', 'font.size': 10})

    print("\n[VISUALIZER] Generating High-Resolution Charts for Data Science Evaluation...")

    # -------------------------------------------------------------------------
    # Chart 1: Category-Wise Product Distribution (Pie / Donut Chart)
    # -------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(9, 7), dpi=200)
    cat_counts = df_products['category_name'].value_counts()
    colors = sns.color_palette('pastel')[0:len(cat_counts)]
    
    wedges, texts, autotexts = ax.pie(
        cat_counts.values, 
        labels=cat_counts.index, 
        autopct='%1.1f%%',
        startangle=140,
        colors=colors,
        wedgeprops=dict(width=0.45, edgecolor='white', linewidth=2),
        pctdistance=0.75
    )
    for at in autotexts:
        at.set_fontsize(9.5)
        at.set_weight('bold')
    for t in texts:
        t.set_fontsize(9.5)
    
    ax.set_title("Category-Wise Product Distribution\n(VCET IT - 25ITC31 Foundations of Data Science)", 
                 fontsize=12, fontweight='bold', pad=15, color='#1A237E')
    
    # Donut center circle text
    ax.text(0, 0, f"Total\n{len(df_products)}\nProducts", ha='center', va='center', fontsize=11, fontweight='bold', color='#37474F')
    
    c1_path = os.path.join(output_dir, "1_category_distribution.png")
    plt.tight_layout()
    plt.savefig(c1_path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"  [1/7] Saved Category Distribution Pie Chart -> {c1_path}")

    # -------------------------------------------------------------------------
    # Chart 2: Product-Wise Sales Performance (Grouped Bar Chart: Units & Revenue)
    # -------------------------------------------------------------------------
    perf = analysis_results['product_performance'].sort_values('total_revenue', ascending=False).head(10)
    fig, ax1 = plt.subplots(figsize=(12, 6.5), dpi=200)

    x = np.arange(len(perf))
    width = 0.38

    color_units = '#1976D2'
    color_rev = '#388E3C'

    rects1 = ax1.bar(x - width/2, perf['units_sold'], width, label='Units Sold', color=color_units, edgecolor='black', alpha=0.85)
    ax1.set_ylabel('Total Units Sold', color=color_units, fontsize=11, fontweight='bold')
    ax1.tick_params(axis='y', labelcolor=color_units)
    ax1.set_xticks(x)
    ax1.set_xticklabels(perf['product_name'], rotation=35, ha='right', fontsize=9)

    ax2 = ax1.twinx()
    rects2 = ax2.bar(x + width/2, perf['total_revenue'], width, label='Total Revenue ($)', color=color_rev, edgecolor='black', alpha=0.85)
    ax2.set_ylabel('Total Revenue ($)', color=color_rev, fontsize=11, fontweight='bold')
    ax2.tick_params(axis='y', labelcolor=color_rev)
    ax2.grid(False)

    plt.title("Top 10 Products: Sales Volume vs. Revenue Performance", fontsize=13, fontweight='bold', pad=15, color='#0D47A1')
    
    # Add values on top of bars
    for rect in rects1:
        h = rect.get_height()
        ax1.annotate(f'{int(h)}', xy=(rect.get_x() + rect.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold')
    for rect in rects2:
        h = rect.get_height()
        ax2.annotate(f'${h:.0f}', xy=(rect.get_x() + rect.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold', color='#1B5E20')

    c2_path = os.path.join(output_dir, "2_product_sales_volume_and_revenue.png")
    plt.tight_layout()
    plt.savefig(c2_path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"  [2/7] Saved Product-Wise Sales Bar Chart -> {c2_path}")

    # -------------------------------------------------------------------------
    # Chart 3: Daily Sales Trend (Line Chart with Rolling Average)
    # -------------------------------------------------------------------------
    daily = analysis_results['daily_sales'].copy()
    daily['sale_date_str'] = daily['sale_date'].astype(str)
    
    fig, ax = plt.subplots(figsize=(11, 6), dpi=200)
    ax.plot(daily['sale_date_str'], daily['daily_revenue'], marker='o', linewidth=2.5, markersize=8, color='#D32F2F', label='Daily Revenue ($)')
    
    # 2-point moving average trend
    daily['rolling_avg'] = daily['daily_revenue'].rolling(window=2, min_periods=1).mean()
    ax.plot(daily['sale_date_str'], daily['rolling_avg'], linestyle='--', linewidth=2, color='#1976D2', label='Moving Trend (2-Period MA)')

    for i, row in daily.iterrows():
        ax.annotate(f"${row['daily_revenue']:.1f}", (row['sale_date_str'], row['daily_revenue']),
                    textcoords="offset points", xytext=(0, 10), ha='center', fontsize=8.5, fontweight='bold', color='#B71C1C')

    ax.set_title("Daily Sales Revenue Trend\n(Course: 25ITC31 Time Series Visualization)", fontsize=13, fontweight='bold', pad=15, color='#B71C1C')
    ax.set_xlabel("Transaction Date", fontsize=11, fontweight='bold')
    ax.set_ylabel("Sales Revenue ($)", fontsize=11, fontweight='bold')
    ax.set_xticklabels(daily['sale_date_str'], rotation=30, ha='right')
    ax.legend(loc='upper left', frameon=True)

    c3_path = os.path.join(output_dir, "3_daily_sales_trends.png")
    plt.tight_layout()
    plt.savefig(c3_path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"  [3/7] Saved Daily Sales Trend Line Chart -> {c3_path}")

    # -------------------------------------------------------------------------
    # Chart 4: Stock Availability Comparison vs. Reorder Level (Bar Chart)
    # -------------------------------------------------------------------------
    sample_stock = df_products.sort_values('available_stock').head(12)
    fig, ax = plt.subplots(figsize=(12, 6.5), dpi=200)

    indices = np.arange(len(sample_stock))
    bar_w = 0.38

    b1 = ax.bar(indices - bar_w/2, sample_stock['available_stock'], bar_w, label='Available Stock Units', color='#0288D1', edgecolor='black')
    b2 = ax.bar(indices + bar_w/2, sample_stock['reorder_level'], bar_w, label='Reorder Threshold Level', color='#FFA000', edgecolor='black')

    ax.set_ylabel('Stock Units', fontsize=11, fontweight='bold')
    ax.set_title("Stock Availability vs. Reorder Level Thresholds (Bottom 12 Products)", fontsize=13, fontweight='bold', pad=15, color='#01579B')
    ax.set_xticks(indices)
    ax.set_xticklabels(sample_stock['product_name'], rotation=40, ha='right', fontsize=8.5)
    ax.legend(loc='upper left')

    # Highlight threshold violations
    for i, (_, row) in enumerate(sample_stock.iterrows()):
        if row['available_stock'] <= row['reorder_level']:
            ax.annotate('⚠️ LOW', xy=(indices[i] - bar_w/2, row['available_stock'] + 1.5),
                        ha='center', fontsize=7.5, fontweight='bold', color='#D32F2F')

    c4_path = os.path.join(output_dir, "4_stock_availability_vs_reorder.png")
    plt.tight_layout()
    plt.savefig(c4_path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"  [4/7] Saved Stock Availability vs. Reorder Chart -> {c4_path}")

    # -------------------------------------------------------------------------
    # Chart 5: Fast-Selling Products Analysis (Horizontal Bar Chart)
    # -------------------------------------------------------------------------
    fast_selling = analysis_results['fast_selling_products'].sort_values('units_sold', ascending=True)
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=200)

    bars = ax.barh(fast_selling['product_name'], fast_selling['units_sold'], color='#43A047', edgecolor='black', height=0.55)
    ax.set_xlabel('Total Units Sold', fontsize=11, fontweight='bold')
    ax.set_title("Top 5 Fast-Selling Products (Ranked by Sales Volume)", fontsize=13, fontweight='bold', pad=15, color='#1B5E20')

    for bar in bars:
        w = bar.get_width()
        ax.text(w + 0.2, bar.get_y() + bar.get_height()/2, f"{int(w)} Units", 
                va='center', fontsize=9, fontweight='bold', color='#1B5E20')

    c5_path = os.path.join(output_dir, "5_fast_selling_products.png")
    plt.tight_layout()
    plt.savefig(c5_path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"  [5/7] Saved Fast-Selling Products Bar Chart -> {c5_path}")

    # -------------------------------------------------------------------------
    # Chart 6: Low-Stock Product Risk Analysis (Diverging/Warning Bar Chart)
    # -------------------------------------------------------------------------
    low_stock_df = analysis_results['low_stock_products'].copy()
    if not low_stock_df.empty:
        low_stock_df['deficit'] = low_stock_df['reorder_level'] - low_stock_df['available_stock']
        fig, ax = plt.subplots(figsize=(10, 5), dpi=200)
        
        palette = ['#C62828' if s == 'CRITICAL' else '#F57C00' for s in low_stock_df['stock_status']]
        bars = ax.bar(low_stock_df['product_name'], low_stock_df['deficit'], color=palette, edgecolor='black', width=0.5)

        ax.set_ylabel('Stock Deficit below Reorder Level', fontsize=11, fontweight='bold')
        ax.set_title("Low-Stock Product Risk Assessment (Deficit to Safety Level)", fontsize=13, fontweight='bold', pad=15, color='#B71C1C')
        ax.set_xticklabels(low_stock_df['product_name'], rotation=25, ha='right', fontsize=9)

        for bar in bars:
            h = bar.get_height()
            ax.annotate(f"-{int(h)} Units", xy=(bar.get_x() + bar.get_width() / 2, h),
                        xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='bold', color='#B71C1C')

        c6_path = os.path.join(output_dir, "6_low_stock_risk_analysis.png")
        plt.tight_layout()
        plt.savefig(c6_path, dpi=200, bbox_inches='tight')
        plt.close()
        print(f"  [6/7] Saved Low-Stock Risk Analysis Chart -> {c6_path}")

    # -------------------------------------------------------------------------
    # Chart 7: Correlation Heatmap (Seaborn Heatmap across Financial/Inventory Metrics)
    # -------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 6.5), dpi=200)
    corr_cols = ['quantity_sold', 'unit_price', 'cost_price', 'subtotal', 'gross_profit', 'profit_margin_pct']
    corr_matrix = df_sales[corr_cols].corr()

    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=1, ax=ax, cbar_kws={'label': 'Correlation Coefficient (r)'})
    ax.set_title("Sales & Financial Feature Correlation Heatmap\n(Course: 25ITC31 Seaborn Heat Maps)", fontsize=12, fontweight='bold', pad=15, color='#311B92')
    ax.set_xticklabels(['Qty Sold', 'Unit Price', 'Cost Price', 'Revenue', 'Gross Profit', 'Margin %'], rotation=30, ha='right')
    ax.set_yticklabels(['Qty Sold', 'Unit Price', 'Cost Price', 'Revenue', 'Gross Profit', 'Margin %'], rotation=0)

    c7_path = os.path.join(output_dir, "7_correlation_matrix_heatmap.png")
    plt.tight_layout()
    plt.savefig(c7_path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"  [7/7] Saved Correlation Matrix Heatmap -> {c7_path}")

    print("[VISUALIZER] All 7 charts successfully rendered and saved to Visualizations directory.")

if __name__ == "__main__":
    from db_extractor import extract_raw_datasets
    from data_preprocessor import clean_and_transform
    from data_analyzer import perform_statistical_analysis
    p, s, _, _ = extract_raw_datasets()
    p_c, s_c = clean_and_transform(p, s)
    res = perform_statistical_analysis(p_c, s_c)
    out = r"d:\nithe\retail store inventory\Retail_Store_Inventory_and_Sales_Analysis_System\4_Foundation_of_Data_Science\Visualizations"
    generate_all_visualizations(p_c, s_c, res, out)

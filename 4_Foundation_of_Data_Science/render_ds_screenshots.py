import os
import sys

sys.path.append(r"d:\nithe\retail store inventory\Retail_Store_Inventory_and_Sales_Analysis_System")
from render_terminal_screenshot import create_terminal_screenshot

DS_DIR = r"d:\nithe\retail store inventory\Retail_Store_Inventory_and_Sales_Analysis_System\4_Foundation_of_Data_Science"
OUT_DIR = os.path.join(DS_DIR, "Output")
SCREENSHOTS_DIR = os.path.join(DS_DIR, "Screenshots")

def generate_ds_screenshots():
    with open(os.path.join(OUT_DIR, "data_science_analysis_output.txt"), 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()

    # 1. Preprocessing Screenshot (First ~35 lines)
    prep_lines = lines[:35]
    create_terminal_screenshot("data_preprocessor.py - Data Cleaning & Outlier Treatment", prep_lines,
                               os.path.join(SCREENSHOTS_DIR, "python_preprocessing_screenshot.png"))

    # 2. EDA Analysis Screenshot (Lines from Phase 3, descriptive stats & tables)
    eda_lines = lines[30:75]
    create_terminal_screenshot("data_analyzer.py - Descriptive Statistics & Fast-Selling Ranking", eda_lines,
                               os.path.join(SCREENSHOTS_DIR, "python_eda_analysis_screenshot.png"))

    # 3. Visualization Generation Screenshot (Phase 4 & visualizer output)
    viz_lines = lines[70:115] if len(lines) > 70 else lines[40:]
    create_terminal_screenshot("visualizer.py - 7 High-Res Matplotlib & Seaborn Charts Rendered", viz_lines,
                               os.path.join(SCREENSHOTS_DIR, "python_visualization_screenshot.png"))

    print("[SUCCESS] All Data Science terminal screenshots generated successfully!")

if __name__ == "__main__":
    generate_ds_screenshots()

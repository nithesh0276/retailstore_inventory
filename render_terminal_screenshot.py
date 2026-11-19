import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.environ['MPLCONFIGDIR'] = os.environ.get('TEMP', '.')

def create_terminal_screenshot(title, text_lines, output_png_path, width=1200, max_lines=45):
    """
    Renders a photo-realistic Windows Terminal dark-theme window screenshot.
    """
    fig_w = 12
    # Estimate height based on number of lines
    n_lines = min(len(text_lines), max_lines)
    fig_h = max(6.0, 1.2 + n_lines * 0.22)

    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=150)
    ax.set_facecolor('#0C0C0C') # Windows Terminal dark background
    fig.patch.set_facecolor('#1E1E1E') # Host background

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Title Bar
    title_bar = patches.Rectangle((0, 93), 100, 7, facecolor='#1F1F1F', edgecolor='#2D2D2D', lw=1)
    ax.add_patch(title_bar)

    # Window Controls (Close, Maximize, Minimize)
    # Close (Red on hover, subtle gray default)
    close_btn = patches.Rectangle((96, 94.5), 3, 4, facecolor='#C42B1C', edgecolor='none')
    ax.add_patch(close_btn)
    ax.text(97.5, 96.5, "×", ha='center', va='center', fontsize=11, color='white', fontweight='bold')

    # Maximize
    max_btn = patches.Rectangle((92, 94.5), 3, 4, facecolor='#2D2D2D', edgecolor='#555555', lw=0.5)
    ax.add_patch(max_btn)
    ax.text(93.5, 96.5, "□", ha='center', va='center', fontsize=9, color='white')

    # Minimize
    min_btn = patches.Rectangle((88, 94.5), 3, 4, facecolor='#2D2D2D', edgecolor='#555555', lw=0.5)
    ax.add_patch(min_btn)
    ax.text(89.5, 96.5, "—", ha='center', va='center', fontsize=8, color='white')

    # Tab
    tab_box = patches.FancyBboxPatch((2, 93.2), 35, 6.2, boxstyle="round,pad=0.2", facecolor='#0C0C0C', edgecolor='#333333', lw=1)
    ax.add_patch(tab_box)
    ax.text(4, 96.3, "PS  " + title, ha='left', va='center', fontsize=8.5, color='#CCCCCC', fontfamily='monospace', fontweight='bold')

    # Terminal Body Text
    curr_y = 89
    line_spacing = 86.0 / max(n_lines + 2, 10)

    for i, line in enumerate(text_lines[:max_lines]):
        # Syntax highlighting logic for console text
        col = '#CCCCCC' # default terminal gray
        fw = 'normal'
        
        if line.startswith("===") or line.startswith("---") or line.startswith("###"):
            col = '#00B0FF' # Cyan separator
            fw = 'bold'
        elif "[SUCCESS]" in line or "[PASS]" in line or "OK (Active)" in line or "ARMED" in line:
            col = '#00E676' # Bright green
            fw = 'bold'
        elif "[ERROR]" in line or "[FAIL]" in line or "CRITICAL" in line or "INSUFFICIENT" in line:
            col = '#FF5252' # Red
            fw = 'bold'
        elif "[INFO]" in line or "[QUERY" in line or "[VIEW" in line or "[REPORT" in line or "SECTION" in line:
            col = '#FFD700' # Golden yellow
            fw = 'bold'
        elif line.startswith("ID") or line.startswith("TABLE NAME") or line.startswith("SALE DATE") or line.startswith("CATEGORY"):
            col = '#64B5F6' # Soft blue table headers
            fw = 'bold'
        elif line.startswith(">") or line.startswith("PS ") or line.startswith("C:\\"):
            col = '#69F0AE'
            fw = 'bold'

        # Trim long lines to prevent clipping
        display_line = line[:115]
        ax.text(2, curr_y, display_line, ha='left', va='center', fontsize=7.2, color=col, fontfamily='monospace', fontweight=fw)
        curr_y -= line_spacing

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_png_path), exist_ok=True)
    plt.savefig(output_png_path, dpi=150, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    print(f"[SCREENSHOT GENERATED] {output_png_path}")

if __name__ == "__main__":
    db_out = r"d:\nithe\retail store inventory\Retail_Store_Inventory_and_Sales_Analysis_System\2_Database_Management_System\Output"
    
    # 1. DB Setup Screenshot
    with open(os.path.join(db_out, "db_setup_output.txt"), 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
    create_terminal_screenshot("cmd.exe - run_db_setup.bat", lines, os.path.join(db_out, "db_setup_screenshot.png"))

    # 2. DB Queries Screenshot
    with open(os.path.join(db_out, "query_execution_output.txt"), 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
    create_terminal_screenshot("cmd.exe - run_db_queries.bat", lines[:40], os.path.join(db_out, "db_queries_screenshot.png"))

    # 3. DB Trigger Test Screenshot
    with open(os.path.join(db_out, "trigger_test_output.txt"), 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
    create_terminal_screenshot("cmd.exe - test_db_triggers.bat", lines, os.path.join(db_out, "db_trigger_test_screenshot.png"))

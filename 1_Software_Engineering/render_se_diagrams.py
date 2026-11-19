import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.environ['MPLCONFIGDIR'] = os.environ.get('TEMP', '.')

BASE_SE_DIR = r"d:\nithe\retail store inventory\Retail_Store_Inventory_and_Sales_Analysis_System\1_Software_Engineering"

def render_use_case():
    fig, ax = plt.subplots(figsize=(12, 8), dpi=200)
    ax.set_xlim(0, 100)
    ax.set_ylim(100, 0) # invert for top-down or keep standard
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    # Title
    ax.text(50, 96, "USE CASE DIAGRAM: RETAIL STORE INVENTORY & SALES ANALYSIS SYSTEM", 
            ha='center', va='center', fontsize=14, fontweight='bold', color='#1A237E')
    ax.text(50, 93, "Academic Regulation: VCET B.Tech IT (R2025) | Course: 25ITT33 Software Engineering",
            ha='center', va='center', fontsize=10, style='italic', color='#455A64')

    # System Boundary Box
    rect = patches.FancyBboxPatch((28, 5), 68, 84, boxstyle="round,pad=1.5", 
                                  linewidth=2, edgecolor="#0277BD", facecolor="#F1F8E9", alpha=0.5)
    ax.add_patch(rect)
    ax.text(62, 86, "System Boundary: Retail Store Core Engine", fontsize=11, fontweight='bold', color="#01579B", ha='center')

    # Actors (Left)
    actors = [
        ("Store Manager", 75, "#D32F2F"),
        ("Cashier / Clerk", 50, "#388E3C"),
        ("Inventory Auditor", 25, "#F57C00"),
        ("Data Analyst", 10, "#7B1FA2")
    ]
    
    for name, y, col in actors:
        circle = plt.Circle((10, y+4), 2.2, color=col, ec='black', lw=1.5)
        ax.add_patch(circle)
        ax.plot([10, 10], [y+1.8, y-3], color='black', lw=2) # body
        ax.plot([5, 15], [y, y], color='black', lw=2) # arms
        ax.plot([10, 6], [y-3, y-7], color='black', lw=2) # left leg
        ax.plot([10, 14], [y-3, y-7], color='black', lw=2) # right leg
        ax.text(10, y-9, name, ha='center', fontsize=9, fontweight='bold', color=col)

    # Use Cases (Ellipses)
    ucs = [
        ("UC-01: Manage Product Catalog", 45, 78, "#E1F5FE", "#0288D1"),
        ("UC-02: Manage Categories", 78, 78, "#E1F5FE", "#0288D1"),
        ("UC-03: Register Customer Details", 45, 64, "#E8F5E9", "#388E3C"),
        ("UC-04: Process Sales Transaction", 78, 64, "#E8F5E9", "#2E7D32"),
        ("UC-05: Check Stock Availability", 45, 50, "#FFF9C4", "#FBC02D"),
        ("UC-06: Prevent Over-Sale", 78, 50, "#FFEBEE", "#E53935"),
        ("UC-07: Auto-Deduct Inventory", 45, 36, "#FFF3E0", "#FB8C00"),
        ("UC-08: Log Stock Movement Audit", 78, 36, "#EDE7F6", "#8E24AA"),
        ("UC-09: Generate Operational Reports", 45, 22, "#E0F7FA", "#00ACC1"),
        ("UC-10: Python Analytics & Visualizations", 78, 22, "#F3E5F5", "#AB47BC")
    ]

    for text, x, y, bg, border in ucs:
        box = patches.FancyBboxPatch((x-14, y-3.5), 28, 7, boxstyle="round,pad=0.8",
                                     fc=bg, ec=border, lw=1.5)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=8.5, fontweight='bold', color='#212121')

    # Associations
    ax.annotate("", xy=(31, 78), xytext=(17, 73), arrowprops=dict(arrowstyle="-", color='#D32F2F', lw=1.5))
    ax.annotate("", xy=(64, 78), xytext=(17, 73), arrowprops=dict(arrowstyle="-", color='#D32F2F', lw=1.5))
    ax.annotate("", xy=(31, 22), xytext=(17, 73), arrowprops=dict(arrowstyle="-", color='#D32F2F', lw=1.5))

    ax.annotate("", xy=(31, 64), xytext=(17, 48), arrowprops=dict(arrowstyle="-", color='#388E3C', lw=1.5))
    ax.annotate("", xy=(64, 64), xytext=(17, 48), arrowprops=dict(arrowstyle="-", color='#388E3C', lw=1.5))
    ax.annotate("", xy=(31, 50), xytext=(17, 48), arrowprops=dict(arrowstyle="-", color='#388E3C', lw=1.5))

    ax.annotate("", xy=(31, 50), xytext=(17, 23), arrowprops=dict(arrowstyle="-", color='#F57C00', lw=1.5))
    ax.annotate("", xy=(31, 22), xytext=(17, 23), arrowprops=dict(arrowstyle="-", color='#F57C00', lw=1.5))

    ax.annotate("", xy=(64, 22), xytext=(17, 9), arrowprops=dict(arrowstyle="-", color='#7B1FA2', lw=1.5))

    ax.annotate("<<include>>", xy=(45, 54), xytext=(68, 62),
                arrowprops=dict(arrowstyle="->", linestyle="dashed", color="#1565C0", lw=1.2),
                fontsize=7.5, color="#0D47A1", fontweight='bold')
    
    ax.annotate("<<include>>", xy=(45, 40), xytext=(70, 60),
                arrowprops=dict(arrowstyle="->", linestyle="dashed", color="#1565C0", lw=1.2),
                fontsize=7.5, color="#0D47A1", fontweight='bold')

    ax.annotate("<<extend>>", xy=(78, 60), xytext=(78, 54),
                arrowprops=dict(arrowstyle="->", linestyle="dashed", color="#C62828", lw=1.2),
                fontsize=7.5, color="#B71C1C", fontweight='bold')

    out_path = os.path.join(BASE_SE_DIR, "Use_Case_Diagram", "use_case_diagram.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=200, bbox_inches='tight')
    plt.close()
    print("Saved Use Case Diagram to:", out_path)

def render_class_diagram():
    fig, ax = plt.subplots(figsize=(14, 9), dpi=200)
    ax.set_xlim(0, 140)
    ax.set_ylim(0, 90)
    ax.axis('off')

    ax.text(70, 87, "UML CLASS DIAGRAM: DOMAIN ENTITIES & SERVICE ARCHITECTURE",
            ha='center', va='center', fontsize=14, fontweight='bold', color='#0D47A1')
    ax.text(70, 84, "VCET B.Tech IT - 25ITT33 Software Engineering | 25ITT32 Java Programming",
            ha='center', va='center', fontsize=10, style='italic', color='#546E7A')

    def draw_class(x, y, w, h, name, attrs, methods, header_col="#1976D2", body_col="#E3F2FD"):
        box = patches.Rectangle((x, y-h), w, h, facecolor=body_col, edgecolor="#37474F", lw=1.5)
        ax.add_patch(box)
        hdr = patches.Rectangle((x, y-3.5), w, 3.5, facecolor=header_col, edgecolor="#37474F", lw=1.5)
        ax.add_patch(hdr)
        ax.text(x + w/2, y - 1.8, name, ha='center', va='center', fontsize=8.5, fontweight='bold', color='white')
        
        curr_y = y - 5.5
        for a in attrs:
            ax.text(x + 1, curr_y, a, fontsize=7, color='#212121')
            curr_y -= 2.2
        ax.plot([x, x+w], [curr_y, curr_y], color='#90A4AE', lw=1)
        curr_y -= 1.8
        for m in methods:
            ax.text(x + 1, curr_y, m, fontsize=7, color='#0D47A1')
            curr_y -= 2.2

    draw_class(5, 78, 25, 22, "Category", 
               ["- categoryId: int", "- categoryName: String", "- description: String"], 
               ["+ getCategoryId(): int", "+ getCategoryName(): String"])
    
    draw_class(38, 78, 30, 26, "Product", 
               ["- productId: int", "- productName: String", "- categoryId: int", "- unitPrice: double", "- costPrice: double", "- reorderLevel: int"], 
               ["+ getProductId(): int", "+ getUnitPrice(): double", "+ isLowStock(): boolean"])

    draw_class(76, 78, 28, 24, "Inventory", 
               ["- inventoryId: int", "- productId: int", "- availableStock: int", "- lastUpdated: String"], 
               ["+ getAvailableStock(): int", "+ deductStock(qty: int)", "+ addStock(qty: int)"])

    draw_class(110, 78, 25, 22, "StockUpdate", 
               ["- updateId: int", "- productId: int", "- changeQty: int", "- updateType: String", "- balanceStock: int"], 
               ["+ getUpdateId(): int", "+ getBalance(): int"])

    draw_class(5, 45, 28, 22, "Customer", 
               ["- customerId: int", "- customerName: String", "- phone: String", "- email: String"], 
               ["+ getCustomerId(): int", "+ getPhone(): String"])

    draw_class(40, 45, 32, 26, "SalesTransaction", 
               ["- transactionId: int", "- customerId: int", "- transactionDate: String", "- totalAmount: double", "- paymentMode: String", "- items: List<SalesDetail>"], 
               ["+ addItem(detail: SalesDetail)", "+ calculateTotal(): double"])

    draw_class(80, 45, 28, 22, "SalesDetail", 
               ["- detailId: int", "- transactionId: int", "- productId: int", "- quantitySold: int", "- unitPrice: double", "- subtotal: double"], 
               ["+ getSubtotal(): double", "+ getQuantity(): int"])

    draw_class(112, 45, 26, 22, "InsufficientStockException",
               ["- productId: int", "- availableQty: int", "- requestedQty: int"],
               ["+ getMessage(): String", "+ getShortfall(): int"],
               header_col="#C62828", body_col="#FFEBEE")

    draw_class(20, 15, 45, 14, "SalesService",
               ["- salesDAO: SalesDAO", "- inventoryDAO: InventoryDAO"],
               ["+ processSale(tx: SalesTransaction): boolean", "+ validateStock(prodId: int, qty: int): boolean"],
               header_col="#2E7D32", body_col="#E8F5E9")

    draw_class(75, 15, 45, 14, "InventoryService",
               ["- inventoryDAO: InventoryDAO", "- productDAO: ProductDAO"],
               ["+ checkStock(prodId: int): int", "+ restockProduct(prodId: int, qty: int): boolean"],
               header_col="#2E7D32", body_col="#E8F5E9")

    # Connectors
    ax.annotate("", xy=(38, 68), xytext=(30, 68), arrowprops=dict(arrowstyle="->", color='#37474F', lw=1.5))
    ax.text(32, 70, "1..*", fontsize=8, fontweight='bold')
    
    ax.annotate("", xy=(76, 68), xytext=(68, 68), arrowprops=dict(arrowstyle="->", color='#37474F', lw=1.5))
    ax.text(71, 70, "1..1", fontsize=8, fontweight='bold')

    ax.annotate("", xy=(110, 68), xytext=(104, 68), arrowprops=dict(arrowstyle="->", color='#37474F', lw=1.5))

    ax.annotate("", xy=(40, 35), xytext=(33, 35), arrowprops=dict(arrowstyle="->", color='#37474F', lw=1.5))

    ax.annotate("", xy=(80, 35), xytext=(72, 35), arrowprops=dict(arrowstyle="->", color='#37474F', lw=1.5))
    diamond = patches.RegularPolygon((72, 35), 4, radius=1.2, orientation=0.785, facecolor='black', edgecolor='black')
    ax.add_patch(diamond)

    ax.annotate("", xy=(94, 45), xytext=(53, 52), arrowprops=dict(arrowstyle="->", linestyle="dashed", color='#1565C0', lw=1.2))

    ax.annotate("", xy=(55, 19), xytext=(55, 15), arrowprops=dict(arrowstyle="->", color='#2E7D32', lw=1.2))
    ax.annotate("", xy=(90, 19), xytext=(90, 15), arrowprops=dict(arrowstyle="->", color='#2E7D32', lw=1.2))

    out_path = os.path.join(BASE_SE_DIR, "Class_Diagram", "class_diagram.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=200, bbox_inches='tight')
    plt.close()
    print("Saved Class Diagram to:", out_path)

def render_activity_diagram():
    fig, ax = plt.subplots(figsize=(10, 11), dpi=200)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 120)
    ax.axis('off')

    ax.text(50, 116, "ACTIVITY DIAGRAM: SALES CHECKOUT & STOCK VALIDATION",
            ha='center', va='center', fontsize=13, fontweight='bold', color='#B71C1C')
    ax.text(50, 113, "Course: 25ITT33 Software Engineering | Decision Logic & Exception Handling",
            ha='center', va='center', fontsize=9.5, style='italic', color='#546E7A')

    start_c = plt.Circle((50, 107), 1.8, color='black')
    ax.add_patch(start_c)
    ax.annotate("", xy=(50, 101), xytext=(50, 105.2), arrowprops=dict(arrowstyle="->", color='black', lw=1.5))

    def draw_act(x, y, text, bg="#E1F5FE", ec="#0288D1", w=36, h=5.5):
        box = patches.FancyBboxPatch((x-w/2, y-h/2), w, h, boxstyle="round,pad=0.5", fc=bg, ec=ec, lw=1.5)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=8, fontweight='bold', color='#212121')

    draw_act(50, 98, "Select Customer & Scan Products")
    ax.annotate("", xy=(50, 91), xytext=(50, 95.2), arrowprops=dict(arrowstyle="->", color='black', lw=1.5))

    draw_act(50, 88, "Input Quantity to Purchase")
    ax.annotate("", xy=(50, 80), xytext=(50, 85.2), arrowprops=dict(arrowstyle="->", color='black', lw=1.5))

    diamond = patches.RegularPolygon((50, 75), 4, radius=4.5, orientation=0.785, facecolor='#FFF9C4', edgecolor='#FBC02D', lw=1.5)
    ax.add_patch(diamond)
    ax.text(50, 75, "Is Stock\nAvailable?", ha='center', va='center', fontsize=7.5, fontweight='bold')

    ax.annotate("[No: Qty > Stock]", xy=(18, 75), xytext=(45, 75), arrowprops=dict(arrowstyle="->", color='#C62828', lw=1.5))
    draw_act(18, 65, "Throw InsufficientStockException\nDisplay Out of Stock Alert", bg="#FFCDD2", ec="#D32F2F", w=32, h=6.5)
    ax.annotate("", xy=(18, 68.25), xytext=(18, 75), arrowprops=dict(arrowstyle="->", color='#C62828', lw=1.5))
    
    draw_act(18, 52, "Prompt User: Adjust Qty or Abort", bg="#FFE0B2", ec="#FB8C00", w=32, h=5.5)
    ax.annotate("", xy=(18, 54.75), xytext=(18, 61.75), arrowprops=dict(arrowstyle="->", color='black', lw=1.5))

    ax.annotate("[Yes: Qty <= Stock]", xy=(50, 65), xytext=(50, 70.5), arrowprops=dict(arrowstyle="->", color='#2E7D32', lw=1.5))
    draw_act(50, 62, "Reserve Item & Calculate Subtotal", bg="#E8F5E9", ec="#388E3C")

    ax.annotate("", xy=(50, 55), xytext=(50, 59.2), arrowprops=dict(arrowstyle="->", color='black', lw=1.5))
    draw_act(50, 52, "Select Payment Mode (Cash/Card/UPI)")

    ax.annotate("", xy=(50, 45), xytext=(50, 49.2), arrowprops=dict(arrowstyle="->", color='black', lw=1.5))
    draw_act(50, 42, "BEGIN DATABASE TRANSACTION", bg="#D1C4E9", ec="#512DA8")

    rect_sub = patches.FancyBboxPatch((28, 20), 44, 18, boxstyle="round,pad=1.0", fc="#EDE7F6", ec="#673AB7", lw=1.5, ls="--")
    ax.add_patch(rect_sub)
    ax.text(50, 36, "Atomic Commit Stage (Database)", ha='center', fontsize=8, fontweight='bold', color='#4A148C')

    draw_act(50, 31, "1. Insert sales_transactions & details", bg="white", ec="#7E57C2", w=38, h=4.2)
    draw_act(50, 25, "2. Trigger: Deduct inventory stock\n3. Trigger: Write stock_updates audit", bg="white", ec="#7E57C2", w=38, h=5)

    ax.annotate("", xy=(50, 39.2), xytext=(50, 38.5), arrowprops=dict(arrowstyle="->", color='black', lw=1.5))
    ax.annotate("", xy=(50, 15), xytext=(50, 20), arrowprops=dict(arrowstyle="->", color='black', lw=1.5))

    draw_act(50, 12, "COMMIT TRANSACTION & Print Receipt", bg="#C8E6C9", ec="#2E7D32", w=38, h=5)

    ax.annotate("", xy=(50, 6), xytext=(50, 9.5), arrowprops=dict(arrowstyle="->", color='black', lw=1.5))
    end_outer = plt.Circle((50, 4.5), 2.2, color='#2E7D32', fill=False, lw=1.8)
    end_inner = plt.Circle((50, 4.5), 1.4, color='#2E7D32')
    ax.add_patch(end_outer)
    ax.add_patch(end_inner)

    out_path = os.path.join(BASE_SE_DIR, "Activity_Diagram", "activity_diagram.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=200, bbox_inches='tight')
    plt.close()
    print("Saved Activity Diagram to:", out_path)

def render_sequence_diagram():
    fig, ax = plt.subplots(figsize=(13, 8), dpi=200)
    ax.set_xlim(0, 130)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(65, 96, "SEQUENCE DIAGRAM: TRANSACTION EXECUTION & AUTOMATIC STOCK REDUCTION",
            ha='center', va='center', fontsize=13, fontweight='bold', color='#1A237E')
    ax.text(65, 93, "Object Interaction between UI, Service, DAO, SQLite Database and Triggers",
            ha='center', va='center', fontsize=9.5, style='italic', color='#546E7A')

    lifelines = [
        ("Cashier", 12, "#E53935"),
        ("RetailStoreApp (UI)", 35, "#1E88E5"),
        ("SalesService", 58, "#43A047"),
        ("InventoryDAO", 80, "#FB8C00"),
        ("SalesDAO", 100, "#8E24AA"),
        ("SQLite Database", 120, "#3949AB")
    ]

    for name, x, col in lifelines:
        box = patches.FancyBboxPatch((x-10, 85), 20, 5, boxstyle="round,pad=0.3", fc=col, ec='black', lw=1.2)
        ax.add_patch(box)
        ax.text(x, 87.5, name, ha='center', va='center', fontsize=7.5, fontweight='bold', color='white')
        ax.plot([x, x], [85, 8], color='#90A4AE', lw=1.2, ls="--")

    msgs = [
        (80, 12, 35, "1: processSale(customerId, prodId, qty)", False),
        (73, 35, 58, "2: validateAndExecute(prodId, qty)", False),
        (66, 58, 80, "3: getAvailableStock(prodId)", False),
        (60, 80, 120, "4: SELECT available_stock", False),
        (54, 120, 80, "5: return available_stock (e.g. 50)", True),
        (48, 80, 58, "6: return availableStock", True),
        (42, 58, 100, "7: recordTransaction(tx)", False),
        (36, 100, 120, "8: BEGIN TRANSACTION; INSERT tx, details", False),
        (30, 120, 120, "9: Trigger: Deduct stock & audit log", False),
        (24, 120, 100, "10: COMMIT; return txId", True),
        (18, 100, 58, "11: Transaction Success", True),
        (12, 58, 35, "12: Display Receipt & Success Alert", True)
    ]

    for y, x1, x2, text, is_ret in msgs:
        ls = "--" if is_ret else "-"
        col = "#1565C0" if not is_ret else "#2E7D32"
        ax.annotate("", xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle="->", color=col, lw=1.3, linestyle=ls))
        mid_x = (x1 + x2) / 2
        ax.text(mid_x, y + 1.5, text, ha='center', fontsize=7.2, fontweight='bold', color='#263238')

    out_path = os.path.join(BASE_SE_DIR, "Sequence_Diagram", "sequence_diagram.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=200, bbox_inches='tight')
    plt.close()
    print("Saved Sequence Diagram to:", out_path)

def render_dfd():
    fig, ax = plt.subplots(figsize=(13, 8), dpi=200)
    ax.set_xlim(0, 130)
    ax.set_ylim(0, 90)
    ax.axis('off')

    ax.text(65, 86, "DATA FLOW DIAGRAM (DFD) LEVEL 1: RETAIL STORE SYSTEM",
            ha='center', va='center', fontsize=14, fontweight='bold', color='#004D40')
    ax.text(65, 82, "Functional Decomposition into Catalog, Sales, Inventory & Analytics Processes",
            ha='center', va='center', fontsize=10, style='italic', color='#546E7A')

    def draw_entity(x, y, name, col="#ECEFF1", ec="#455A64"):
        box = patches.Rectangle((x-10, y-4), 20, 8, facecolor=col, edgecolor=ec, lw=1.5)
        ax.add_patch(box)
        ax.text(x, y, name, ha='center', va='center', fontsize=8, fontweight='bold')

    def draw_proc(x, y, num, name, col="#B2DFDB", ec="#00796B"):
        circle = plt.Circle((x, y), 6, facecolor=col, edgecolor=ec, lw=1.5)
        ax.add_patch(circle)
        ax.text(x, y+1.8, num, ha='center', fontsize=8, fontweight='bold', color='#004D40')
        ax.text(x, y-1.5, name, ha='center', fontsize=6.8, fontweight='bold', color='#004D40')

    def draw_store(x, y, id_name, label):
        ax.plot([x-12, x+12], [y+3, y+3], color='#37474F', lw=1.5)
        ax.plot([x-12, x+12], [y-3, y-3], color='#37474F', lw=1.5)
        ax.plot([x-12, x-12], [y-3, y+3], color='#37474F', lw=1.5)
        ax.text(x-7, y, id_name, ha='center', va='center', fontsize=7, fontweight='bold', color='#D84315')
        ax.text(x+4, y, label, ha='center', va='center', fontsize=7, fontweight='bold', color='#263238')

    draw_entity(15, 65, "Cashier / POS")
    draw_entity(15, 25, "Store Manager")
    draw_entity(115, 45, "Data Analyst")

    draw_proc(45, 65, "2.0", "Verify Stock &\nProcess Sale")
    draw_proc(45, 25, "1.0", "Manage\nCatalog")
    draw_proc(80, 65, "3.0", "Auto Update\nInventory")
    draw_proc(80, 25, "4.0", "Generate\nReports")
    draw_proc(85, 45, "5.0", "Python\nAnalytics")

    draw_store(45, 45, "D1", "Products & Cats")
    draw_store(80, 82, "D2", "Inventory Store")
    draw_store(80, 7, "D3", "Sales Records")

    ax.annotate("Order (Items, Qty)", xy=(39, 65), xytext=(25, 65), arrowprops=dict(arrowstyle="->", color='#00796B', lw=1.3), fontsize=7)
    ax.annotate("Sales Receipt", xy=(25, 62), xytext=(39, 62), arrowprops=dict(arrowstyle="->", color='#00796B', lw=1.3), fontsize=7)
    
    ax.annotate("Catalog Updates", xy=(39, 25), xytext=(25, 25), arrowprops=dict(arrowstyle="->", color='#00796B', lw=1.3), fontsize=7)
    ax.annotate("Save Product", xy=(45, 41), xytext=(45, 31), arrowprops=dict(arrowstyle="->", color='#00796B', lw=1.3), fontsize=7)

    ax.annotate("Stock Level", xy=(45, 59), xytext=(45, 49), arrowprops=dict(arrowstyle="<->", color='#00796B', lw=1.3), fontsize=7)
    ax.annotate("Record Tx", xy=(49, 61), xytext=(76, 11), arrowprops=dict(arrowstyle="->", color='#00796B', lw=1.3), fontsize=7)

    ax.annotate("Trigger Decrement", xy=(74, 65), xytext=(51, 65), arrowprops=dict(arrowstyle="->", color='#D84315', lw=1.3), fontsize=7)
    ax.annotate("Update Stock", xy=(80, 78), xytext=(80, 71), arrowprops=dict(arrowstyle="->", color='#D84315', lw=1.3), fontsize=7)

    ax.annotate("Extract Data", xy=(85, 40), xytext=(82, 11), arrowprops=dict(arrowstyle="->", color='#5E35B1', lw=1.3), fontsize=7)
    ax.annotate("Charts & Insights", xy=(105, 45), xytext=(91, 45), arrowprops=dict(arrowstyle="->", color='#5E35B1', lw=1.3), fontsize=7)

    out_path = os.path.join(BASE_SE_DIR, "DFD", "dfd_diagram.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=200, bbox_inches='tight')
    plt.close()
    print("Saved DFD to:", out_path)

def render_architecture():
    fig, ax = plt.subplots(figsize=(12, 8), dpi=200)
    ax.set_xlim(0, 120)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(60, 96, "SYSTEM ARCHITECTURE: 4-TIER ENTERPRISE LAYERED ARCHITECTURE",
            ha='center', va='center', fontsize=13, fontweight='bold', color='#283593')
    ax.text(60, 92, "Separation of Presentation, Business Logic, Persistence & Analytical Subsystems",
            ha='center', va='center', fontsize=9.5, style='italic', color='#546E7A')

    layers = [
        ("Tier 1: Presentation Layer", 82, 10, "#E8EAF6", "#3F51B5", 
         ["Java Console Dashboard (Interactive CLI)", "Automated Demo Runner", "Python Visualizer & Report Displays"]),
        ("Tier 2: Business Logic & Service Layer", 62, 10, "#E8F5E9", "#2E7D32", 
         ["SalesService (Stock Pre-Check & Validation)", "InventoryService (Restock & Alert Rules)", "ReportService (Java 8+ Streams)"]),
        ("Tier 3: Data Access & Persistence Layer (DAO)", 42, 10, "#FFF3E0", "#E65100", 
         ["CategoryDAO | ProductDAO | CustomerDAO", "InventoryDAO | SalesDAO (JDBC Parameterized Queries)", "Singleton DBConnection Manager & Python sqlite3"]),
        ("Tier 4: Relational Database Management Layer", 20, 14, "#EDE7F6", "#512DA8", 
         ["SQLite Core Engine (retail_store.db)", "7 Relational Tables (3NF)", "Automated Triggers (Over-Sale Check & Auto Stock Decrement)", "Analytical Views (Daily Sales, Low Stock, Product Performance)"])
    ]

    for title, y, h, bg, ec, items in layers:
        box = patches.FancyBboxPatch((15, y-h), 90, h, boxstyle="round,pad=1.0", fc=bg, ec=ec, lw=1.8)
        ax.add_patch(box)
        ax.text(18, y - 2, title, fontsize=9.5, fontweight='bold', color=ec)
        
        item_y = y - 5.5
        for itm in items:
            ax.text(22, item_y, "• " + itm, fontsize=8, color='#263238')
            item_y -= 2.6

    ax.annotate("", xy=(60, 72), xytext=(60, 68), arrowprops=dict(arrowstyle="<->", color='#37474F', lw=1.8))
    ax.annotate("", xy=(60, 52), xytext=(60, 48), arrowprops=dict(arrowstyle="<->", color='#37474F', lw=1.8))
    ax.annotate("", xy=(60, 32), xytext=(60, 26), arrowprops=dict(arrowstyle="<->", color='#37474F', lw=1.8))

    out_path = os.path.join(BASE_SE_DIR, "Architecture_Diagram", "architecture_diagram.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=200, bbox_inches='tight')
    plt.close()
    print("Saved Architecture Diagram to:", out_path)

if __name__ == "__main__":
    render_use_case()
    render_class_diagram()
    render_activity_diagram()
    render_sequence_diagram()
    render_dfd()
    render_architecture()
    print("All SE diagrams rendered successfully!")

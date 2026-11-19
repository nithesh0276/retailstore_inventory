import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.environ['MPLCONFIGDIR'] = os.environ.get('TEMP', '.')

BASE_DB_DIR = r"d:\nithe\retail store inventory\Retail_Store_Inventory_and_Sales_Analysis_System\2_Database_Management_System"

def render_er_diagram():
    fig, ax = plt.subplots(figsize=(14, 10), dpi=200)
    ax.set_xlim(0, 140)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Title
    ax.text(70, 96, "ENTITY-RELATIONSHIP (E-R) DIAGRAM: RETAIL STORE DATABASE",
            ha='center', va='center', fontsize=14, fontweight='bold', color='#B71C1C')
    ax.text(70, 93, "Course: 25ITT31 Database Management Systems | Entity Sets, Cardinalities & Key Attributes",
            ha='center', va='center', fontsize=9.5, style='italic', color='#546E7A')

    # Helper function for Entity Box
    def draw_entity(x, y, w, h, name, attrs, pk_attr, fk_attrs=None, col="#FFCDD2", ec="#C62828"):
        if fk_attrs is None:
            fk_attrs = []
        box = patches.FancyBboxPatch((x, y-h), w, h, boxstyle="round,pad=0.5", fc=col, ec=ec, lw=1.8)
        ax.add_patch(box)
        # Header
        hdr = patches.Rectangle((x, y-4), w, 4, fc=ec, ec=ec)
        ax.add_patch(hdr)
        ax.text(x + w/2, y-2, name, ha='center', va='center', fontsize=8.5, fontweight='bold', color='white')
        
        curr_y = y - 6.5
        for a in attrs:
            prefix = ""
            font_w = 'normal'
            txt_col = '#212121'
            if a == pk_attr:
                prefix = "[PK] "
                font_w = 'bold'
                txt_col = '#B71C1C'
            elif a in fk_attrs:
                prefix = "[FK] "
                font_w = 'bold'
                txt_col = '#1565C0'
            ax.text(x + 1.5, curr_y, prefix + a, fontsize=7.2, fontweight=font_w, color=txt_col)
            curr_y -= 2.4

    # Helper function for Relationship Diamond
    def draw_rel(x, y, text, col="#FFE082", ec="#FF8F00"):
        diamond = patches.RegularPolygon((x, y), 4, radius=3.8, orientation=0.785, facecolor=col, edgecolor=ec, lw=1.5)
        ax.add_patch(diamond)
        ax.text(x, y, text, ha='center', va='center', fontsize=6.8, fontweight='bold', color='#E65100')

    # Entities
    draw_entity(5, 85, 26, 20, "CATEGORY", 
                ["category_id", "category_name", "description"], 
                "category_id")

    draw_entity(46, 85, 32, 28, "PRODUCT",
                ["product_id", "product_name", "category_id", "unit_price", "cost_price", "reorder_level"],
                "product_id", ["category_id"])

    draw_entity(93, 85, 28, 22, "INVENTORY",
                ["inventory_id", "product_id", "available_stock", "last_updated"],
                "inventory_id", ["product_id"], col="#C8E6C9", ec="#2E7D32")

    draw_entity(100, 52, 28, 24, "STOCK_UPDATE",
                ["update_id", "product_id", "change_qty", "update_type", "balance_stock", "update_time"],
                "update_id", ["product_id"], col="#FFF9C4", ec="#FBC02D")

    draw_entity(5, 45, 28, 24, "CUSTOMER",
                ["customer_id", "customer_name", "phone", "email", "address"],
                "customer_id", col="#E1BEE7", ec="#7B1FA2")

    draw_entity(45, 45, 34, 28, "SALES_TRANSACTION",
                ["transaction_id", "customer_id", "transaction_date", "total_amount", "payment_mode", "cashier_name"],
                "transaction_id", ["customer_id"], col="#BBDEFB", ec="#1976D2")

    draw_entity(46, 12, 32, 26, "SALES_DETAILS",
                ["detail_id", "transaction_id", "product_id", "quantity_sold", "unit_price", "subtotal"],
                "detail_id", ["transaction_id", "product_id"], col="#FFE0B2", ec="#F57C00")

    # Relationships (Diamonds)
    draw_rel(38.5, 75, "Classifies")
    draw_rel(85.5, 75, "Has_Stock")
    draw_rel(36.5, 33, "Places")
    draw_rel(62, 22, "Contains")
    draw_rel(89, 22, "Sold_As")
    draw_rel(90, 50, "Audits")

    # Connector Lines with Cardinalities
    # Category -- Classifies -- Product (1 : N)
    ax.plot([31, 34.7], [75, 75], color='#37474F', lw=1.5)
    ax.text(32, 76.5, "1", fontsize=8.5, fontweight='bold')
    ax.plot([42.3, 46], [75, 75], color='#37474F', lw=1.5)
    ax.text(43.5, 76.5, "N", fontsize=8.5, fontweight='bold')

    # Product -- Has_Stock -- Inventory (1 : 1)
    ax.plot([78, 81.7], [75, 75], color='#37474F', lw=1.5)
    ax.text(79, 76.5, "1", fontsize=8.5, fontweight='bold')
    ax.plot([89.3, 93], [75, 75], color='#37474F', lw=1.5)
    ax.text(90.5, 76.5, "1", fontsize=8.5, fontweight='bold')

    # Customer -- Places -- Sales_Transaction (1 : N)
    ax.plot([33, 33], [33, 33], color='#37474F', lw=1.5)
    ax.plot([33, 32.7], [33, 33], color='#37474F', lw=1.5)
    ax.plot([33, 33.7], [33, 33], color='#37474F', lw=1.5)
    ax.plot([40.3, 45], [33, 33], color='#37474F', lw=1.5)
    ax.text(34, 34.5, "1", fontsize=8.5, fontweight='bold')
    ax.text(42.5, 34.5, "N", fontsize=8.5, fontweight='bold')

    # Sales_Transaction -- Contains -- Sales_Details (1 : N)
    ax.plot([62, 62], [17, 18.2], color='#37474F', lw=1.5)
    ax.plot([62, 62], [25.8, 12], color='#37474F', lw=1.5)
    ax.text(63, 27, "1", fontsize=8.5, fontweight='bold')
    ax.text(63, 14, "N", fontsize=8.5, fontweight='bold')

    # Product to Sales_Details (1 : N via Sold_As)
    ax.plot([62, 62], [57, 57], color='#37474F', lw=1.5)
    ax.plot([78, 89], [57, 26], color='#37474F', lw=1.5, ls=":")
    ax.plot([89, 78], [22, 12], color='#37474F', lw=1.5, ls=":")

    # Product to Stock_Update (1 : N via Audits)
    ax.plot([78, 86.2], [62, 50], color='#37474F', lw=1.5)
    ax.text(80, 58, "1", fontsize=8.5, fontweight='bold')
    ax.plot([93.8, 100], [50, 50], color='#37474F', lw=1.5)
    ax.text(96, 51.5, "N", fontsize=8.5, fontweight='bold')

    out_path = os.path.join(BASE_DB_DIR, "ER_Diagram", "er_diagram.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=200, bbox_inches='tight')
    plt.close()
    print("Saved ER Diagram to:", out_path)

if __name__ == "__main__":
    render_er_diagram()

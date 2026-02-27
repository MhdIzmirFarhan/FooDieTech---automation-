# gui_v2.py
import tkinter as tk
from tkinter import filedialog
import threading
import pandas as pd
from config import set_restaurant, restaurant_list
import os
import sys

if getattr(sys, 'frozen', False):
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = os.path.join(
        sys._MEIPASS, "ms-playwright"
    )

# ---------------- IMPORT PAGE FUNCTIONS ----------------
from Pages.create_page.create_item_page import open_food_item_page
from Pages.edit_page.edit_page import open_edit_item_page
from Pages.analyze_page import open_analysis_page
from Pages.delete_page import open_delete_dashboard
from Pages.inventory_page.supplier_page import open_supplier_page
from Pages.employee_page.employee_section_page import open_employee_section_page 

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("Foodiee Menu Automation")
root.state('zoomed')  # Fullscreen

# ---------------- GLOBAL STATE ----------------
selected_file_path = tk.StringVar(value="")
restaurant_var = tk.StringVar(value=restaurant_list[0])

# ---------------- STATUS LABEL ----------------
status_label = tk.Label(root, text="Ready", fg="green", font=("Segoe UI", 12, "bold"))
status_label.pack(side="bottom", fill="x", pady=5)

# ---------------- HEADER ----------------
header_frame = tk.Frame(root, pady=10)
header_frame.pack(fill="x")

tk.Label(
    header_frame,
    text="Foodiee Menu Automation",
    font=("Segoe UI", 20, "bold")
).pack()

# ---------------- RESTAURANT SELECT ----------------
def on_restaurant_change(*args):
    set_restaurant(restaurant_var.get())

restaurant_var.trace_add("write", on_restaurant_change)

restaurant_frame = tk.Frame(root, pady=10)
restaurant_frame.pack(fill="x")

tk.Label(restaurant_frame, text="Restaurant:", font=("Segoe UI", 12, "bold")).pack(side="left", padx=10)
restaurant_dropdown = tk.OptionMenu(restaurant_frame, restaurant_var, *restaurant_list)
restaurant_dropdown.config(width=30, font=("Segoe UI", 12))
restaurant_dropdown.pack(side="left")

# ---------------- INSTRUCTIONS ----------------
instructions = (
    "How to use:\n"
    "1. Select your restaurant from the dropdown\n"
    "2. Click an action button below\n"
    "3. Upload Excel when prompted\n"
    "4. Wait until the process completes\n\n"
    "Buttons:\n"
    "🍔 Add  – Create new food items\n"
    "✏️ Edit – Update existing items\n"
    "🔍 Analyze – Compare Excel vs system\n"
    "🗑 Delete – Remove items or data\n"
    "🧾 Supplier – Bulk create suppliers\n"
    "👤 Employee – Employee management (coming soon)"
)

tk.Label(
    root,
    text=instructions,
    font=("Segoe UI", 11),
    justify="left",
    fg="#555",
    padx=20,
    pady=10
).pack(fill="x")

# ---------------- ACTION BUTTONS ----------------
btn_frame = tk.Frame(root, pady=20)
btn_frame.pack()

button_font = ("Segoe UI", 14, "bold")
button_width = 18
button_height = 2

# Row 0: Main action buttons (2x3 grid)
tk.Button(
    btn_frame, text="🍔 Add", width=button_width, height=button_height, font=button_font,
    command=lambda: open_food_item_page(selected_file_path.get(), status_label)
).grid(row=0, column=0, padx=20, pady=10)

tk.Button(
    btn_frame, text="✏️ Edit", width=button_width, height=button_height, font=button_font,
    command=lambda: open_edit_item_page(status_label)
).grid(row=0, column=1, padx=20, pady=10)

tk.Button(
    btn_frame, text="🔍 Analyze", width=button_width, height=button_height, font=button_font,
    command=lambda: open_analysis_page(selected_file_path, status_label)
).grid(row=0, column=2, padx=20, pady=10)

tk.Button(
    btn_frame, text="🗑 Delete", width=button_width, height=button_height, font=button_font,
    command=lambda: open_delete_dashboard()
).grid(row=1, column=0, padx=20, pady=10)

tk.Button(
    btn_frame, text="🧾 Supplier", width=button_width, height=button_height, font=button_font,
    command=lambda: open_supplier_page(None, None)
).grid(row=1, column=1, padx=20, pady=10)

tk.Button(
    btn_frame,
    text="👤 Employee",
    width=button_width,
    height=button_height,
    font=button_font,
    command=open_employee_section_page  # no parentheses
).grid(row=1, column=2, padx=20, pady=10)

# ---------------- ROW 2: Delete + Excel ----------------
import pandas as pd
from tkinter import filedialog

def create_excel_template(status_label=None):
    """Create an Excel template with predefined sheets and columns based on your project."""

    file_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel Files", "*.xlsx")],
        title="Save Excel Template"
    )
    if not file_path:
        return

    # ---------------- Define sheets and their columns ----------------
    sheets = {
        "Items": [
            "food", "price", "category", "kitchen", "sessions",
            "add_ons", "img", "extra_notes", "max_extra_notes_limit"
        ],
        "extra_notes": [
            "note_name"
        ],
        "Sessions": [
            "session_name", "description", "from_time", "to_time", "status"
        ],
        "Add-ons": [
            "add_ons_name", "price", "status"
        ],
        "Category": [
            "category_name"
        ],
        "Kitchen": [
            "kitchenname", "ip_address", "port"
        ],
        "Suppliers": [
            "supplier_name", "contact_person", "phone", "email", "address",
            "gst_number", "payment_terms", "credit_limit", "rating", "bank_details"
        ],
        "Inventory": [
            "item_code", "item_name", "item_type", "category", "description",
            "barcode", "brand", "model", "image", "uom", "purchase_uom",
            "conversion_ratio", "min_stock", "max_stock", "reorder_level",
            "location", "shelf_life", "storage_temperature"
        ],
        "edit": [
            # =============================
            # ITEM REFERENCE
            # =============================
            "ref_food_name",
        
            # =============================
            # ITEM EDIT FIELDS
            # =============================
            "food", "price", "category", 
            "kitchen", "sessions", "add_ons", 
            "img", "extra_notes", "max_extra_notes_limit",
        
            # =============================
            # ADD-ON REFERENCE & EDIT
            # =============================
            "reference_addon",        # existing addon name (search key)
            "addon_name",       # new addon name
            "price",      # new price
            "status",     # Active / Inactive
        
            # =============================
            # CATEGORY REFERENCE & EDIT
            # =============================
            "ref_category",
            "category_name",
            "parent_category",
            "is_web",
            "is_open_item"
        ],
        "Table": [
            "table_name",
            "capacity",
            "floor",
            "image"
        ],
        "Employees": [
            "name",
            "last_name",
            "email",
            "phone",
            "country",
            "state",
            "city",
            "zip_code",
            "division_type",
            "designation",
            "duty_type",
            "original_hire_date",
            "termination_reason",
            "rate",
            "hire_date",
            "termination_voluntary",
            "termination_reason_type",
            "pay_frequency",
            "supervisor_name",
            "is_supervisor",
            "supervisor_report",
            "date_of_birth",
            "marital_status",
            "live_in_state",
            "gender",
            "work_in_state",
            "citizen",
            "photograph",
            "emergency_contact",
            "emergency_home_phone",
            "emergency_work_phone"
        ],

        "Attendance": [
            "employee_id",
            "date",
            "sign_in",
            "sign_out",
            "staytime"
        ],
    }

    # ---------------- Create Excel ----------------
    with pd.ExcelWriter(file_path) as writer:
        for sheet_name, columns in sheets.items():
            df = pd.DataFrame(columns=columns)
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    # ---------------- Notify user ----------------
    msg = f"✅ Excel template created: {file_path}"
    if status_label:
        status_label.config(text=msg, fg="green")
    print(msg)

tk.Button(
    btn_frame,
    text="📄 Create Excel", width=20,
    bg="#2980b9", fg="white",
    font=("Segoe UI", 12, "bold"),
    command=create_excel_template
).grid(row=2, column=2, columnspan=1, pady=10, padx=10)

# ---------------- START APP ----------------
root.mainloop()

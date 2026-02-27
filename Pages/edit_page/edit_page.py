# Pages/edit_page/edit_page.py

import tkinter as tk
from tkinter import filedialog
import threading

# ---------------- GLOBAL ----------------
selected_file_path = None


# ---------------- FILE UPLOAD ----------------
def upload_file(file_label, status_label):
    global selected_file_path

    file_path = filedialog.askopenfilename(
        title="Select Excel / CSV File",
        filetypes=[("Excel Files", "*.xlsx *.csv")]
    )

    if not file_path:
        return

    selected_file_path = file_path
    file_label.config(text=file_path, fg="#2c3e50")
    status_label.config(text="✅ File loaded successfully", fg="green")


# ---------------- DUMMY BOT FUNCTION ----------------
def run_edit_bot(options):
    if not selected_file_path:
        print("❌ No file uploaded")
        return

    # FOOD ITEM EDITOR
    if options.get("items"):
        from Functions.Edit.edit_details import edit_items_from_excel
        edit_items_from_excel(selected_file_path)

    # CATEGORY EDITOR
    if options.get("category"):
        from Functions.Edit.edit_cetgory import edit_categories_from_excel
        edit_categories_from_excel(selected_file_path)

    # ADDONS EDITOR
    if options.get("addons"):
        from Functions.Edit.edit_addons import edit_addons_from_excel
        edit_addons_from_excel(selected_file_path)





# ---------------- MAIN UI ----------------
def open_edit_item_page(main_status_label):
    edit_win = tk.Toplevel()
    edit_win.title("Edit Food Items")
    edit_win.state("zoomed")  # FULLSCREEN

    # ================= HEADER =================
    header = tk.Frame(edit_win, pady=20)
    header.pack(fill="x")

    tk.Label(
        header,
        text="Edit Food Items",
        font=("Segoe UI", 18, "bold")
    ).pack()

    tk.Label(
        header,
        text="Upload Excel and choose what to update",
        font=("Segoe UI", 10),
        fg="gray"
    ).pack(pady=(5, 0))

    # ================= FILE SECTION =================
    file_frame = tk.LabelFrame(
        edit_win,
        text=" Excel File ",
        font=("Segoe UI", 10, "bold"),
        padx=20,
        pady=15
    )
    file_frame.pack(fill="x", padx=40, pady=20)

    file_label = tk.Label(
        file_frame,
        text="No file selected",
        fg="gray",
        anchor="w",
        wraplength=900
    )
    file_label.pack(fill="x")

    page_status = tk.Label(
        file_frame,
        text="",
        font=("Segoe UI", 10)
    )
    page_status.pack(anchor="w", pady=(8, 0))

    tk.Button(
        file_frame,
        text="📂 Upload Excel / CSV",
        width=24,
        bg="#3498db",
        fg="white",
        font=("Segoe UI", 10),
        command=lambda: upload_file(file_label, page_status)
    ).pack(pady=10)

    # ================= OPTIONS =================
    options_frame = tk.LabelFrame(
        edit_win,
        text=" What do you want to edit? ",
        font=("Segoe UI", 10, "bold"),
        padx=30,
        pady=20
    )
    options_frame.pack(fill="x", padx=40, pady=10)

    # BooleanVars
    opt_items = tk.BooleanVar()
    opt_category = tk.BooleanVar()
    opt_addons = tk.BooleanVar()
   

    def option_checkbox(text, var):
        return tk.Checkbutton(
            options_frame,
            text=text,
            variable=var,
            font=("Segoe UI", 11),
            anchor="w"
        )

    option_checkbox("🍽 Item", opt_items).grid(row=0, column=0, sticky="w", pady=6)
    option_checkbox("📁 Category", opt_category).grid(row=1, column=0, sticky="w", pady=6)
    option_checkbox("➕ Add-ons", opt_addons).grid(row=2, column=0, sticky="w", pady=6)

    # ================= ACTION =================
    action_frame = tk.Frame(edit_win, pady=30)
    action_frame.pack()

    def start_edit():
        if not selected_file_path:
            page_status.config(text="❌ Please upload a file first", fg="red")
            return
    
        options = {
            "category": opt_category.get(),
            "addons": opt_addons.get(),
            "items": opt_items.get(),
        }
    
        page_status.config(text="✏️ Running edit automation...", fg="#2980b9")
        main_status_label.config(text="Editing food items...", fg="#2980b9")
    
        # Run in separate thread to not freeze UI
        threading.Thread(
            target=run_edit_bot,
            args=(options,),
            daemon=True
        ).start()


    tk.Button(
        action_frame,
        text="▶ Run Edit Automation",
        width=28,
        height=2,
        bg="#f39c12",
        fg="white",
        font=("Segoe UI", 11, "bold"),
        command=start_edit
    ).pack()

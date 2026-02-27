import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as messagebox
import threading

from Functions.Inventory.supplier import create_suppliers
from Pages.inventory_page import items_page, categorty_item_page


def open_supplier_page(upload_file, selected_file_path):
    print("File:", selected_file_path)

    supplier_win = tk.Toplevel()
    supplier_win.title("Bulk Supplier Management")
    supplier_win.geometry("560x460")
    supplier_win.resizable(False, False)
    supplier_win.configure(bg="#f4f6f8")

    # -----------------------------
    # MAIN CARD
    # -----------------------------
    card = tk.Frame(
        supplier_win,
        bg="white",
        bd=0,
        relief="flat"
    )
    card.place(relx=0.5, rely=0.5, anchor="center", width=520, height=420)

    # -----------------------------
    # HEADER
    # -----------------------------
    header = tk.Label(
        card,
        text="Bulk Create Suppliers",
        font=("Segoe UI", 16, "bold"),
        bg="white",
        fg="#2c3e50"
    )
    header.pack(pady=(20, 5))

    sub_header = tk.Label(
        card,
        text="Upload an Excel or CSV file to create suppliers",
        font=("Segoe UI", 10),
        bg="white",
        fg="#7f8c8d"
    )
    sub_header.pack(pady=(0, 15))

    # -----------------------------
    # FILE DISPLAY
    # -----------------------------
    file_frame = tk.Frame(card, bg="#f9fafb", bd=1, relief="solid")
    file_frame.pack(padx=20, pady=10, fill="x")

    file_label = tk.Label(
        file_frame,
        text="No file selected",
        bg="#f9fafb",
        fg="#7f8c8d",
        anchor="w",
        padx=10,
        wraplength=460
    )
    file_label.pack(fill="x", pady=10)

    # -----------------------------
    # STATUS LABEL
    # -----------------------------
    status_label = tk.Label(
        card,
        text="",
        bg="white",
        fg="#2980b9",
        font=("Segoe UI", 9)
    )
    status_label.pack(pady=(5, 10))

    # -----------------------------
    # FILE UPLOAD
    # -----------------------------
    def select_file():
        nonlocal selected_file_path
        path = filedialog.askopenfilename(
            title="Select Supplier Excel / CSV",
            filetypes=[
                ("Excel Files", "*.xlsx *.xls"),
                ("CSV Files", "*.csv")
            ]
        )

        if path:
            selected_file_path = path
            file_label.config(text=path, fg="#2c3e50")
            status_label.config(text="✅ File loaded successfully", fg="#27ae60")

    tk.Button(
        card,
        text="📂 Upload Excel / CSV",
        font=("Segoe UI", 10, "bold"),
        bg="#ecf0f1",
        fg="#2c3e50",
        bd=0,
        height=2,
        cursor="hand2",
        command=select_file
    ).pack(pady=10, padx=60, fill="x")

    # -----------------------------
    # RUN CREATION
    # -----------------------------
    def start_creation():
        if not selected_file_path:
            status_label.config(
                text="❌ Please upload an Excel or CSV file",
                fg="#e74c3c"
            )
            return

        status_label.config(
            text="🚀 Creating suppliers...",
            fg="#2980b9"
        )

        def task():
            try:
                create_suppliers(selected_file_path)
                status_label.config(
                    text="✅ Suppliers created successfully",
                    fg="#27ae60"
                )
            except Exception as e:
                status_label.config(
                    text="❌ Error occurred",
                    fg="#e74c3c"
                )
                messagebox.showerror("Error", str(e))

        threading.Thread(target=task, daemon=True).start()

    tk.Button(
        card,
        text="▶ Create Suppliers",
        font=("Segoe UI", 11, "bold"),
        bg="#27ae60",
        fg="white",
        bd=0,
        height=2,
        cursor="hand2",
        command=start_creation
    ).pack(pady=(10, 15), padx=60, fill="x")

    # -----------------------------
    # ACTION BUTTONS
    # -----------------------------
    action_frame = tk.Frame(card, bg="white")
    action_frame.pack(pady=10, fill="x", padx=40)

    tk.Button(
        action_frame,
        text="📦 Inventory Items",
        font=("Segoe UI", 10, "bold"),
        bg="#2980b9",
        fg="white",
        bd=0,
        height=2,
        cursor="hand2",
        command=lambda: items_page.open_inventory_items_page(lambda x: None, selected_file_path)
    ).pack(side="left", expand=True, fill="x", padx=(0, 10))

    tk.Button(
        action_frame,
        text="🗂 Create Category",
        font=("Segoe UI", 10, "bold"),
        bg="#8e44ad",
        fg="white",
        bd=0,
        height=2,
        cursor="hand2",
        command=lambda: categorty_item_page.open_category_page()
    ).pack(side="right", expand=True, fill="x", padx=(10, 0))

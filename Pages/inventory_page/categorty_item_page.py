# Pages/inventory_page/category_page.py

import tkinter as tk
from tkinter import messagebox
import threading

from Functions.Inventory.items import create_inventory_items

def open_category_page():
    category_win = tk.Toplevel()
    category_win.title("Add Item Category")
    category_win.geometry("400x300")
    category_win.resizable(False, False)

    tk.Label(
        category_win,
        text="Add Inventory Category",
        font=("Segoe UI", 13, "bold")
    ).pack(pady=15)

    # -----------------------------
    # CATEGORY NAME
    # -----------------------------
    tk.Label(category_win, text="Category Name *").pack(pady=5)
    category_name_entry = tk.Entry(category_win, width=40)
    category_name_entry.pack()

    # -----------------------------
    # PARENT CATEGORY
    # -----------------------------
    tk.Label(category_win, text="Parent Category").pack(pady=5)
    parent_var = tk.StringVar()
    parent_options = ["", "Ingredients", "Vessels & Utensils", "Equipment", "Supplies"]
    parent_menu = tk.OptionMenu(category_win, parent_var, *parent_options)
    parent_menu.config(width=30)
    parent_menu.pack()

    # -----------------------------
    # STATUS LABEL
    # -----------------------------
    status_label = tk.Label(category_win, text="", fg="blue")
    status_label.pack(pady=10)

    # -----------------------------
    # SAVE FUNCTION
    # -----------------------------
    def save_category():
        name = category_name_entry.get().strip()
        parent = parent_var.get().strip()
        parent_id = None

        # Map parent name to ID (adjust based on your real IDs)
        parent_mapping = {
            "Ingredients": 1,
            "Vessels & Utensils": 6,
            "Equipment": 7,
            "Supplies": 8
        }

        if parent in parent_mapping:
            parent_id = parent_mapping[parent]

        if not name:
            status_label.config(text="❌ Category name is required", fg="red")
            return

        status_label.config(text="🚀 Creating category...", fg="blue")

        def task():
            try:
                create_category(name, parent_id)
                status_label.config(text="✅ Category created successfully", fg="green")
            except Exception as e:
                status_label.config(text="❌ Error occurred", fg="red")
                messagebox.showerror("Error", str(e))

        threading.Thread(target=task, daemon=True).start()

    tk.Button(
        category_win,
        text="💾 Save Category",
        width=25,
        bg="#2980b9",
        fg="white",
        command=save_category
    ).pack(pady=20)

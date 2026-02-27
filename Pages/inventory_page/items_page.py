import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as messagebox
import threading

from Functions.Inventory.items import create_inventory_items


def open_inventory_items_page(upload_file, selected_file_path):
    print("File:", selected_file_path)

    items_win = tk.Toplevel()
    items_win.title("Create Inventory Items")
    items_win.geometry("520x320")
    items_win.resizable(False, False)

    # -----------------------------
    # TITLE
    # -----------------------------
    tk.Label(
        items_win,
        text="Bulk Create Inventory Items",
        font=("Segoe UI", 13, "bold")
    ).pack(pady=15)

    # -----------------------------
    # FILE LABEL
    # -----------------------------
    file_label = tk.Label(
        items_win,
        text="No file selected",
        fg="gray",
        wraplength=480
    )
    file_label.pack(pady=5)

    # -----------------------------
    # STATUS
    # -----------------------------
    status_label = tk.Label(
        items_win,
        text="",
        fg="blue"
    )
    status_label.pack(pady=5)

    # -----------------------------
    # FILE UPLOAD
    # -----------------------------
    def select_file():
        nonlocal selected_file_path
        path = filedialog.askopenfilename(
            title="Select Inventory Item Excel / CSV",
            filetypes=[
                ("Excel Files", "*.xlsx *.xls"),
                ("CSV Files", "*.csv")
            ]
        )

        if path:
            selected_file_path = path
            file_label.config(text=path, fg="black")
            status_label.config(text="✅ File loaded", fg="green")

    tk.Button(
        items_win,
        text="📂 Upload Excel / CSV",
        width=25,
        command=select_file
    ).pack(pady=5)

    # -----------------------------
    # RUN CREATION
    # -----------------------------
    def start_creation():
        if not selected_file_path:
            status_label.config(
                text="❌ Please upload an Excel or CSV file",
                fg="red"
            )
            return

        status_label.config(
            text="🚀 Creating inventory items...",
            fg="blue"
        )

        def task():
            try:
                create_inventory_items(selected_file_path)
                status_label.config(
                    text="✅ Inventory items created successfully",
                    fg="green"
                )
            except Exception as e:
                status_label.config(
                    text="❌ Error occurred",
                    fg="red"
                )
                messagebox.showerror("Error", str(e))

        threading.Thread(target=task, daemon=True).start()

    tk.Button(
        items_win,
        text="▶ Create Inventory Items",
        width=25,
        bg="#2980b9",
        fg="white",
        command=start_creation
    ).pack(pady=25)

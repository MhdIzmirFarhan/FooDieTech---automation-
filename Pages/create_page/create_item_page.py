from Functions.Create.create_item import create_items
from Functions.Create.add_ons import add_addons
from Functions.Create.add_session import create_sessions_from_excel
from Functions.Create.create_category import create_categories_from_excel
from Functions.Create.extra_notes import create_extra_notes_from_excel
from Functions.Create.create_kitchen import create_kitchens_from_excel

import tkinter as tk
from tkinter import filedialog
import threading
import os

def open_food_item_page(selected_file_path, status_label):
    # ---------------- WINDOW ----------------
    food_win = tk.Toplevel()
    food_win.title("Create New Food Item")
    food_win.geometry("520x520")
    food_win.resizable(True, True)

    # ---------------- LOCAL STATE ----------------
    file_path_var = tk.StringVar(value=selected_file_path)

    # ---------------- UI ----------------
    tk.Label(
        food_win,
        text="Upload Excel / CSV File",
        font=("Segoe UI", 12, "bold")
    ).pack(pady=(10, 5))

    file_label = tk.Label(
        food_win,
        text=file_path_var.get() or "No file selected",
        wraplength=480,
        fg="gray"
    )
    file_label.pack(pady=5)

    page_status = tk.Label(food_win, text="", fg="blue")
    page_status.pack(pady=5)

    # ---------------- FILE PICKER ----------------
    def choose_file():
        path = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel Files", "*.xlsx *.csv")]
        )
        if path:
            file_path_var.set(path)
            file_label.config(text=os.path.basename(path), fg="green")
            status_label.config(
                text=f"Selected file: {os.path.basename(path)}",
                fg="blue"
            )

    tk.Button(
        food_win,
        text="📂 Upload File",
        width=20,
        command=choose_file
    ).pack(pady=8)

    # ---------------- RUN FOOD ITEM ONLY ----------------
    def start_food_bot():
        file_path = file_path_var.get()
        if not file_path:
            page_status.config(text="❌ Please select an Excel file", fg="red")
            return

        page_status.config(text="🚀 Creating food items...", fg="green")
        status_label.config(text="Creating food items...", fg="green")

        def run():
            try:
                create_items(file_path)
                page_status.config(text="✅ Food items created", fg="green")
                status_label.config(text="Done", fg="green")
            except Exception as e:
                page_status.config(text=f"❌ Error: {e}", fg="red")
                status_label.config(text="Error occurred", fg="red")

        threading.Thread(target=run, daemon=True).start()

    tk.Button(
        food_win,
        text="▶ Run Food Items Only",
        width=20,
        bg="#2ecc71",
        fg="white",
        command=start_food_bot
    ).pack(pady=10)

    # ==================================================
    # 🔹 RUN ALL AUTOMATION BUTTON (NEW)
    # ==================================================
    def run_all():
        file_path = file_path_var.get()
        if not file_path:
            page_status.config(text="❌ Please select an Excel file", fg="red")
            return

        page_status.config(text="🚀 Running ALL automations...", fg="green")
        status_label.config(text="Running full setup...", fg="green")

        def run():
            try:
                create_categories_from_excel(file_path)
                add_addons(file_path)
                create_sessions_from_excel(file_path)
                create_extra_notes_from_excel(file_path)
                create_kitchens_from_excel(file_path)
                create_items(file_path)

                page_status.config(
                    text="✅ ALL automations completed successfully",
                    fg="green"
                )
                status_label.config(text="All done 🎉", fg="green")

            except Exception as e:
                page_status.config(text=f"❌ Error: {e}", fg="red")
                status_label.config(text="Error occurred", fg="red")

        threading.Thread(target=run, daemon=True).start()

    tk.Button(
        food_win,
        text="🚀 Run ALL (Category + Add-ons + Session + Notes + Kitchen + Food)",
        width=52,
        bg="#e67e22",
        fg="white",
        command=run_all
    ).pack(pady=15)

    # ==================================================
    # 🔹 QUICK CREATE SECTION (Individual)
    # ==================================================
    tk.Label(
        food_win,
        text="Quick Create (Individual)",
        font=("Segoe UI", 11, "bold")
    ).pack(pady=(10, 5))

    quick_frame = tk.Frame(food_win)
    quick_frame.pack(pady=5)

    def run_simple(fn, label_text):
        file_path = file_path_var.get()
        if not file_path:
            page_status.config(text="❌ Please select an Excel file", fg="red")
            return
        page_status.config(text=f"🚀 {label_text}...", fg="green")
        status_label.config(text=label_text, fg="green")
        threading.Thread(target=lambda: fn(file_path), daemon=True).start()

    tk.Button(
        quick_frame,
        text="📂 Category",
        width=14,
        command=lambda: run_simple(create_categories_from_excel, "Creating Categories")
    ).grid(row=0, column=0, padx=5, pady=5)

    tk.Button(
        quick_frame,
        text="➕ Add-on",
        width=14,
        command=lambda: run_simple(add_addons, "Creating Add-ons")
    ).grid(row=0, column=1, padx=5, pady=5)

    tk.Button(
        quick_frame,
        text="🕒 Session",
        width=14,
        command=lambda: run_simple(create_sessions_from_excel, "Creating Sessions")
    ).grid(row=1, column=0, padx=5, pady=5)

    tk.Button(
        quick_frame,
        text="📝 Extra Notes",
        width=14,
        command=lambda: run_simple(create_extra_notes_from_excel, "Creating Extra Notes")
    ).grid(row=1, column=1, padx=5, pady=5)

    tk.Button(
        quick_frame,
        text="🍳 Kitchen",
        width=14,
        command=lambda: run_simple(create_kitchens_from_excel, "Creating Kitchen")
    ).grid(row=2, column=0, columnspan=2, pady=5)

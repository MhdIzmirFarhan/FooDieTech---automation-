# gui_v2.py
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import threading
from config import set_restaurant, restaurant_list

# ---------------- IMPORT PAGE FUNCTIONS ----------------
from Pages.create_page.create_item_page import open_food_item_page
from Pages.edit_page.edit_page import open_edit_item_page
from Pages.analyze_page import open_analysis_page
from Pages.delete_page import open_delete_all_items, delete_all_assigned_addons, delete_all_orders

# ---------------- BASE PATH ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("Foodiee Menu Automation")
root.geometry("500x360")
root.minsize(400, 300)
root.resizable(True, True)

tk.Label(
    root,
    text="Foodiee Menu Automation",
    font=("Segoe UI", 14, "bold")
).pack(pady=10)

# ---------------- RESTAURANT SELECT DROPDOWN ----------------
restaurant_var = tk.StringVar()
restaurant_var.set(restaurant_list[0])

def on_restaurant_change(*args):
    selected = restaurant_var.get()
    set_restaurant(selected)


restaurant_var.trace_add("write", on_restaurant_change)

restaurant_frame = tk.Frame(root)
restaurant_frame.pack(pady=8)

tk.Label(
    restaurant_frame,
    text="Restaurant:",
    font=("Segoe UI", 10, "bold")
).pack(side="left", padx=5)

restaurant_dropdown = tk.OptionMenu(
    restaurant_frame,
    restaurant_var,
    *restaurant_list
)

restaurant_dropdown.config(
    width=25,
    font=("Segoe UI", 10)
)

restaurant_dropdown.pack(side="left")


# ---------------- GLOBAL STATE ----------------
selected_file_path = tk.StringVar(value="")

# ---------------- STATUS LABEL ----------------
status_label = tk.Label(root, text="Ready", fg="green")
status_label.pack(pady=6)

# ---------------- LOAD ICONS ----------------
def load_icon(filename, size=(36, 36)):
    path = os.path.join(BASE_DIR, "icons", filename)
    img = Image.open(path).resize(size)
    return ImageTk.PhotoImage(img)

icon_create  = load_icon("add.png")
icon_edit    = load_icon("pencil.png")
icon_analyze = load_icon("checked.png")
icon_delete  = load_icon("delete.png")

# ---------------- ICON BUTTON FRAME ----------------
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

# 🍔 CREATE
tk.Button(
    btn_frame,
    image=icon_create,
    command=lambda: open_food_item_page(
        selected_file_path.get(),
        status_label
    )
).grid(row=0, column=0, padx=15)

# ✏️ EDIT
tk.Button(
    btn_frame,
    image=icon_edit,
    command=lambda: open_edit_item_page(status_label)
).grid(row=0, column=1, padx=15)

# 🔍 ANALYZE
tk.Button(
    btn_frame,
    image=icon_analyze,
    command=lambda: open_analysis_page(
        selected_file_path.get(),
        status_label
    )
).grid(row=0, column=2, padx=15)

# 🗑 DELETE ALL ITEMS
tk.Button(
    btn_frame,
    image=icon_delete,
    command=lambda: open_delete_all_items(status_label)
).grid(row=0, column=3, padx=15)

# ==================================================
# 🔥 DELETE ASSIGNED ADD-ONS BUTTON
# ==================================================
def run_delete_assigned_addons():
    status_label.config(text="🗑 Deleting assigned add-ons...", fg="red")
    threading.Thread(
        target=delete_all_assigned_addons,
        args=(status_label,),
        daemon=True
    ).start()

tk.Button(
    root,
    text="🗑 Delete Assigned Add-ons",
    width=30,
    bg="#e74c3c",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    command=run_delete_assigned_addons
).pack(pady=10)

tk.Button(
    btn_frame,
    text="🧾 Delete Orders",
    width=18,
    bg="#c0392b",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    command=lambda: threading.Thread(
        target=delete_all_orders,
        args=(status_label,),
        daemon=True
    ).start()
).grid(row=1, column=0, columnspan=4, pady=10)

# ---------------- START APP ----------------
root.mainloop()

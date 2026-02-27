import tkinter as tk
from tkinter import messagebox
import threading

from Functions.Delete.delete_items import delete_all_items
from Functions.Delete.delete_all_addons import delete_all_assigned_addons  
from Functions.Delete.delete_all_tables import delete_all_tables
from Functions.Delete.delete_all_orders import delete_all_orders

# ==================================================
# 🗑 DELETE DASHBOARD UI
# ==================================================
def open_delete_dashboard():
    root = tk.Toplevel()
    root.title("Danger Zone")
    root.state("zoomed")   # Full screen
    root.configure(bg="#0f172a")  # Dark blue-gray

    # ---------------- TITLE ----------------
    title = tk.Label(
        root,
        text="⚠ DANGER ZONE",
        font=("Segoe UI", 28, "bold"),
        bg="#0f172a",
        fg="#f87171"
    )
    title.pack(pady=(40, 10))

    subtitle = tk.Label(
        root,
        text="Permanent deletion actions — proceed carefully",
        font=("Segoe UI", 14),
        bg="#0f172a",
        fg="#94a3b8"
    )
    subtitle.pack(pady=(0, 30))

    # ---------------- STATUS LABEL ----------------
    status_label = tk.Label(
        root,
        text="Ready",
        font=("Segoe UI", 12),
        bg="#020617",
        fg="#22c55e",
        padx=20,
        pady=10
    )
    status_label.pack(pady=10)

    # ---------------- BUTTON FRAME ----------------
    container = tk.Frame(root, bg="#0f172a")
    container.pack(expand=True)

    # Common button style
    def danger_button(parent, text, command):
        return tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 14, "bold"),
            bg="#dc2626",
            fg="white",
            activebackground="#991b1b",
            activeforeground="white",
            bd=0,
            width=28,
            height=2,
            cursor="hand2"
        )

    # ---------------- BUTTON ACTIONS (PLACEHOLDERS) ----------------
    def delete_items():
        confirm = messagebox.askyesno(
            "⚠ DELETE ALL ITEMS",
            "This will permanently delete ALL items.\n\nAre you sure?"
        )
        if not confirm:
            return
    
        status_label.config(text="🗑 Deleting all items...", fg="#f87171")
    
        def run():
            try:
                delete_all_items()
                status_label.config(text="✅ All items deleted", fg="#4ade80")
            except Exception as e:
                status_label.config(text=f"❌ Error: {e}", fg="#f87171")
    
        threading.Thread(target=run, daemon=True).start()
    

    def delete_addons():
        confirm = messagebox.askyesno(
            "⚠ DELETE ALL ADD-ONS",
            "This will permanently delete ALL add-ons.\n\nAre you sure?"
        )
        if not confirm:
            return
    
        status_label.config(text="🗑 Deleting all add-ons...", fg="#f87171")
    
        def run():
            try:
                delete_all_assigned_addons(status_label)
                status_label.config(text="✅ All add-ons deleted", fg="#4ade80")
            except Exception as e:
                status_label.config(text=f"❌ Error: {e}", fg="#f87171")
    
        threading.Thread(target=run, daemon=True).start()
    
    def delete_tables():
        confirm = messagebox.askyesno(
            "⚠ DELETE ALL TABLES",
            "This will permanently delete ALL tables.\n\nAre you sure?"
        )
        if not confirm:
            return
    
        status_label.config(text="🗑 Deleting all tables...", fg="#f87171")
    
        def run():
            try:
                delete_all_tables()
                status_label.config(text="✅ All tables deleted", fg="#4ade80")
            except Exception as e:
                status_label.config(text=f"❌ Error: {e}", fg="#f87171")
    
        threading.Thread(target=run, daemon=True).start()

    def delete_orders():
        confirm = messagebox.askyesno(
            "⚠ DELETE ALL ORDERS",
            "This will permanently delete ALL orders.\n\nAre you sure?"
        )
        if not confirm:
            return
    
        status_label.config(text="🗑 Deleting all orders...", fg="#f87171")
    
        def run():
            try:
                delete_all_orders(status_label)
                status_label.config(text="✅ All orders deleted", fg="#4ade80")
            except Exception as e:
                status_label.config(text=f"❌ Error: {e}", fg="#f87171")
    
        threading.Thread(target=run, daemon=True).start()
    
    # ---------------- BUTTON GRID ----------------
    btn1 = danger_button(container, "🗑 DELETE ALL ITEMS", delete_items)
    btn2 = danger_button(container, "🗑 DELETE ALL ADD-ONS", delete_addons)
    btn3 = danger_button(container, "🗑 DELETE ALL TABLES", delete_tables)
    btn4 = danger_button(container, "🗑 DELETE ALL ORDERS", delete_orders)

    btn1.grid(row=0, column=0, padx=20, pady=15)
    btn2.grid(row=1, column=0, padx=20, pady=15)
    btn3.grid(row=2, column=0, padx=20, pady=15)
    btn4.grid(row=3, column=0, padx=20, pady=15)

    # ---------------- FOOTER ----------------
    footer = tk.Label(
        root,
        text="These actions cannot be undone",
        font=("Segoe UI", 10),
        bg="#0f172a",
        fg="#64748b"
    )
    footer.pack(pady=20)

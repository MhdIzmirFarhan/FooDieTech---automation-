# # Pages/delete_page/delete_all_items_page.py

# from tkinter import messagebox
# import threading
# from Functions.Delete.delete_all import delete_all_items
# from playwright.sync_api import sync_playwright
# from main import restaurant, login
# import time


# def open_delete_all_items(status_label):
#     confirm = messagebox.askyesno(
#         "⚠ DELETE ALL ITEMS",
#         "This will permanently delete ALL food items.\n\nAre you sure?"
#     )

#     if not confirm:
#         status_label.config(text="Delete cancelled", fg="gray")
#         return

#     status_label.config(text="🗑 Deleting all items...", fg="red")

#     def run_delete():
#         try:
#             delete_all_items()
#             status_label.config(text="✅ All items deleted successfully", fg="green")
#         except Exception as e:
#             status_label.config(text=f"❌ Error: {e}", fg="red")

#     threading.Thread(
#         target=run_delete,
#         daemon=True
#     ).start()

from tkinter import messagebox
import threading
import time
from playwright.sync_api import sync_playwright
from main import login


from Functions.Delete.delete_all import delete_all_items
from Functions.Delete.delete_all import delete_all_assigned_addons


def open_delete_all_items(status_label):
    confirm = messagebox.askyesno(
        "⚠ DELETE ALL ITEMS",
        "This will permanently delete ALL food items.\n\nAre you sure?"
    )

    if not confirm:
        status_label.config(text="Delete cancelled", fg="gray")
        return

    status_label.config(text="🗑 Deleting all items...", fg="red")

    def run_delete():
        try:
            delete_all_items()
            status_label.config(text="✅ All items deleted successfully", fg="green")
        except Exception as e:
            status_label.config(text=f"❌ Error: {e}", fg="red")

    threading.Thread(target=run_delete, daemon=True).start()


# ==================================================
# 🔥 NEW FUNCTION: DELETE ALL ASSIGNED ADD-ONS
# ==================================================
def open_delete_all_assigned_addons(status_label):
    confirm = messagebox.askyesno(
        "⚠ DELETE ASSIGNED ADD-ONS",
        "This will delete ALL assigned add-ons.\n\nAre you sure?"
    )

    if not confirm:
        status_label.config(text="Delete cancelled", fg="gray")
        return

    status_label.config(text="🗑 Deleting assigned add-ons...", fg="red")

    def run_delete():
        try:
            delete_all_assigned_addons()
            status_label.config(
                text="✅ All assigned add-ons deleted",
                fg="green"
            )
        except Exception as e:
            status_label.config(text=f"❌ Error: {e}", fg="red")

    threading.Thread(target=run_delete, daemon=True).start()

def delete_all_orders(status_label):
    URL = "https://eltacoexpress2.foodiee.com.my/ordermanage/order/orderlist"

    status_label.config(text="🗑 Deleting all orders...", fg="red")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        context = browser.new_context()
        page = context.new_page()

        # -----------------------------
        # LOGIN
        # -----------------------------
        login(
            page,
            email="admin@gmail.com",
            password="FooDiee#25!"
        )

        # -----------------------------
        # OPEN ORDER LIST
        # -----------------------------
        page.goto(URL, timeout=60000)
        page.wait_for_timeout(2000)

        # -----------------------------
        # AUTO-ACCEPT ALERT
        # -----------------------------
        page.on("dialog", lambda dialog: dialog.accept())

        # -----------------------------
        # DELETE LOOP
        # -----------------------------
        while True:
            rows = page.locator("td.sorting_1")

            if rows.count() == 0:
                status_label.config(
                    text="✅ All orders deleted",
                    fg="green"
                )
                break

            # 1️⃣ CLICK FIRST ROW NUMBER (EXPAND)
            rows.first.click()
            page.wait_for_timeout(800)

            # 2️⃣ FIND DELETE BUTTON INSIDE CHILD ROW
            delete_btn = page.locator(
                "td.child a.btn-danger i.fa-trash"
            ).first

            if delete_btn.count() == 0:
                # If no delete found, reload and retry
                page.reload()
                page.wait_for_timeout(1500)
                continue

            # 3️⃣ CLICK DELETE
            delete_btn.click()
            time.sleep(1)

            # 4️⃣ RELOAD AFTER DELETE
            page.reload()
            page.wait_for_timeout(1500)

        browser.close()

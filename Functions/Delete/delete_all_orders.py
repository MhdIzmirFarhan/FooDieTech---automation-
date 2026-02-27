import time
from playwright.sync_api import sync_playwright
from main import login
import config

def delete_all_orders(status_label):
    URL = f"https://{config.restaurant}.foodiee.com.my/ordermanage/order/orderlist"

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

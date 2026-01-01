from playwright.sync_api import sync_playwright
import time
from main import login
import config

def delete_all_items():
    INDEX_URL = f"https://{config}.foodiee.com.my/itemmanage/item_food/index"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=120)
        context = browser.new_context()
        page = context.new_page()

        # LOGIN FIRST
        login(
            page,
            email="admin@gmail.com",
            password="FooDiee#25!"
        )

        page.goto(INDEX_URL, timeout=60000)
        page.wait_for_selector("table", timeout=60000)

        deleted_count = 0

        while True:
            # Find all delete buttons
            delete_buttons = page.locator("a.btn.btn-danger")

            if delete_buttons.count() == 0:
                break  # no more items

            # Always delete the first item in list
            page.once("dialog", lambda dialog: dialog.accept())

            delete_buttons.first.click()
            deleted_count += 1

            # Wait for table to reload
            page.wait_for_timeout(1500)
            page.reload()
            page.wait_for_selector("table", timeout=60000)

        browser.close()

    print(f"\n🗑 Deleted {deleted_count} items successfully")

from playwright.sync_api import sync_playwright
from main import login
import config
import time


def delete_all_assigned_addons(status_label):
    URL = f"https://{config.restaurant}.foodiee.com.my/itemmanage/menu_addons/assignaddons"

    status_label.config(text="🗑 Deleting assigned add-ons...", fg="red")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=80)
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
        # OPEN ASSIGN ADDONS PAGE
        # -----------------------------
        page.goto(URL, timeout=60000)
        page.wait_for_timeout(2000)

        # -----------------------------
        # HANDLE CONFIRM DIALOG
        # -----------------------------
        def handle_dialog(dialog):
            dialog.accept()

        page.on("dialog", handle_dialog)

        # -----------------------------
        # LOOP DELETE BUTTONS
        # -----------------------------
        while True:
            delete_buttons = page.locator("a.btn-danger")

            if delete_buttons.count() == 0:
                status_label.config(
                    text="✅ All assigned add-ons deleted",
                    fg="green"
                )
                break

            # Always delete first button
            delete_buttons.first.click()
            time.sleep(1)

            page.reload()
            page.wait_for_timeout(1500)

        browser.close()


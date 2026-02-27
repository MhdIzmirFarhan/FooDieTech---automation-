from playwright.sync_api import sync_playwright
import time
from main import login
import config

def delete_all_items():
    INDEX_URL = f"https://{config.restaurant}.foodiee.com.my/itemmanage/item_food/index"

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

from playwright.sync_api import sync_playwright
import time
from main import login   # assuming this logs in and returns page
import config

INDEX_URL = f"https://{config.restaurant}.foodiee.com.my/setting/restauranttable/index"

def delete_all_tables():
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

        # ---------------- GO TO TABLE PAGE ----------------
        page.goto(INDEX_URL, wait_until="networkidle")
        page.wait_for_load_state("networkidle")

        print("🪑 Deleting all tables...")

        while True:
            delete_buttons = page.locator(
                "a.btn.btn-danger.btn-sm:has(i.fa-trash-o)"
            )

            count = delete_buttons.count()
            if count == 0:
                break

            # Always delete the FIRST one
            btn = delete_buttons.first

            # Handle JS confirm popup
            page.once("dialog", lambda dialog: dialog.accept())

            btn.click()

            # Wait for page to refresh after delete
            page.wait_for_load_state("networkidle")
            time.sleep(0.5)

        print("✅ All tables deleted successfully")

        context.close()
        browser.close()

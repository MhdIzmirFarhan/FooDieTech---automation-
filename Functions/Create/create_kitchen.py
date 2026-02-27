from playwright.sync_api import sync_playwright
import pandas as pd
import time
from main import login
import config


def create_kitchens_from_excel(file_path):
    URL = f"https://{config.restaurant}.foodiee.com.my/setting/kitchensetting/index"

    # -----------------------------
    # READ EXCEL / CSV
    # -----------------------------
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path, sheet_name="Kitchen")

    required_cols = {"kitchenname", "ip_address", "port"}

    if not required_cols.issubset(df.columns):
        print("❌ Excel must contain: kitchenname, ip_address, port")
        return

    # -----------------------------
    # PLAYWRIGHT
    # -----------------------------
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=80)
        context = browser.new_context()
        page = context.new_page()

        # LOGIN
        login(
            page,
            email="admin@gmail.com",
            password="FooDiee#25!"
        )

        # OPEN KITCHEN SETTINGS PAGE
        page.goto(URL, timeout=60000)
        page.wait_for_selector("button:has-text('Add Kitchen')", timeout=60000)

        # -----------------------------
        # LOOP KITCHENS
        # -----------------------------
        for _, row in df.iterrows():

            kitchenname = "" if pd.isna(row["kitchenname"]) else str(row["kitchenname"]).strip()
            ip_address = "" if pd.isna(row["ip_address"]) else str(row["ip_address"]).strip()
            port = "" if pd.isna(row["port"]) else str(row["port"]).strip()

            if not kitchenname or not ip_address or not port:
                print("⏭️ Missing kitchen data → skipping row")
                continue

            print(f"➕ Adding kitchen: {kitchenname}")

            # CLICK "ADD KITCHEN" BUTTON (OPENS MODAL)
            page.click("button:has-text('Add Kitchen')")

            # WAIT FOR MODAL INPUTS
            page.wait_for_selector("input[name='kitchenname']", timeout=5000)

            # FILL FORM
            page.fill("input[name='kitchenname']", kitchenname)
            page.fill("input[name='ip_address']", ip_address)
            page.fill("input[name='port']", port)

            # SUBMIT
            page.click("button[type='submit']")

            print(f"✅ Kitchen created: {kitchenname}")
            time.sleep(2)

        print("\n🎉 All kitchens processed")
        input("Press Enter to close browser...")
        browser.close()

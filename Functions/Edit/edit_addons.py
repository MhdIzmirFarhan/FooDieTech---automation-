import pandas as pd
import time
from playwright.sync_api import sync_playwright
from main import login
import config


def edit_addons_from_excel(file_path):
    ADDON_URL = f"https://{config.restaurant}.foodiee.com.my/itemmanage/menu_addons"

    # -----------------------------
    # READ EXCEL
    # -----------------------------
    try:
        df = pd.read_excel(file_path, sheet_name="edit")
    except ValueError:
        print("❌ Sheet 'addons' not found")
        return

    required_cols = {
        "reference_addon",
        "addon_name",
        "price",
    }

    if not required_cols.issubset(df.columns):
        print("❌ Excel missing required columns")
        return

    # -----------------------------
    # PLAYWRIGHT
    # -----------------------------
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=80)
        context = browser.new_context()
        page = context.new_page()

        # LOGIN
        login(page, "admin@gmail.com", "FooDiee#25!")

        # OPEN ADDON LIST
        page.goto(ADDON_URL, timeout=60000)
        page.wait_for_selector("input[type='search']", timeout=10000)

        # -----------------------------
        # LOOP EXCEL
        # -----------------------------
        for _, row in df.iterrows():
            ref_addon = str(row["reference_addon"]).strip()
            new_name = str(row["addon_name"]).strip()
            price = str(row["price"]).replace("RM", "").strip()

            print(f"\n✏️ Editing addon: {ref_addon} → {new_name}")

            # SEARCH
            search = page.locator("input[type='search']")
            search.fill("")
            search.fill(ref_addon)
            time.sleep(1)

            rows = page.locator("#DataTables_Table_0 tbody tr")

            if rows.count() == 0:
                print(f"❌ Addon not found: {ref_addon}")
                continue

            # CLICK UPDATE ✏️
            rows.first.locator("a[title='Update']").click()

            # WAIT FORM (wait for the REAL input)
            page.wait_for_selector("input[name='addonsname']", timeout=10000)
            
            # -----------------------------
            # UPDATE FIELDS
            # -----------------------------
            if new_name:
                page.fill("input[name='addonsname']", "")
                page.type("input[name='addonsname']", new_name, delay=30)
            
            if price:
                page.fill("input[name='addonsprice']", "")
                page.type("input[name='addonsprice']", price, delay=30)
            
            # SAVE
            page.click("button[type='submit']")
            print(f"✅ Updated addon: {new_name}")
            
            time.sleep(2)
            
            # BACK TO LIST
            page.goto(ADDON_URL, timeout=60000)
            page.wait_for_selector("input[type='search']", timeout=10000)

        print("\n🎉 All addons processed")
        input("Press Enter to close browser...")
        browser.close()

from playwright.sync_api import sync_playwright
import pandas as pd
import time
from main import login
import config


def analyze_items_from_excel(file_path):
    ITEM_LIST_URL = f"https://{config.restaurant}.foodiee.com.my/itemmanage/item_food"

    # -----------------------------
    # READ EXCEL / CSV
    # -----------------------------
    df = pd.read_csv(file_path) if file_path.endswith(".csv") else pd.read_excel(file_path)

    required_cols = {"food", "price"}
    if not required_cols.issubset(df.columns):
        print("❌ Excel must contain columns: food, price")
        return

    excel_items = {
        str(row["food"]).strip(): str(row["price"]).strip()
        for _, row in df.iterrows()
        if str(row["food"]).strip()
    }

    system_items = {}

    # -----------------------------
    # SEARCH + OPEN ITEM (SAME AS EDIT)
    # -----------------------------
    def search_and_open(page, food_name):
        page.goto(ITEM_LIST_URL, timeout=60000)

        search_box = page.locator("#DataTables_Table_0_filter input[type='search']")
        search_box.wait_for(state="visible", timeout=10000)

        search_box.fill("")
        search_box.fill(food_name)
        time.sleep(1)

        rows = page.locator("tbody tr")
        if rows.count() == 0:
            print(f"❌ Not found in system: {food_name}")
            return False

        rows.first.locator("a").first.click()
        page.wait_for_selector("input[name='foodname']", timeout=10000)
        return True

    # -----------------------------
    # PLAYWRIGHT
    # -----------------------------
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=80)
        context = browser.new_context()
        page = context.new_page()

        login(page, email="admin@gmail.com", password="FooDiee#25!")

        for food_name, excel_price in excel_items.items():
            print(f"\n🔍 Checking: {food_name}")

            if not search_and_open(page, food_name):
                continue

            food = page.locator("input[name='foodname']").input_value().strip()
            price = page.locator("input[name='foodprice']").input_value().strip()

            system_items[food] = price

        browser.close()

    # -----------------------------
    # COMPARISON
    # -----------------------------
    missing_items = []
    wrong_items = []

    for name, excel_price in excel_items.items():
        if name not in system_items:
            missing_items.append(name)
        elif system_items[name] != excel_price:
            wrong_items.append(
                f"{name} | Excel: {excel_price} | System: {system_items[name]}"
            )

    extra_items = [
        name for name in system_items
        if name not in excel_items
    ]

    # -----------------------------
    # REPORT
    # -----------------------------
    print("\n📊 ANALYSIS REPORT")
    print("=" * 45)

    if missing_items:
        print("\n❌ Missing in system:")
        for i in missing_items:
            print(f" - {i}")
    else:
        print("\n✅ No missing items")

    if wrong_items:
        print("\n⚠️ Price mismatch:")
        for w in wrong_items:
            print(f" - {w}")
    else:
        print("\n✅ No price mismatches")

    if extra_items:
        print("\n➕ Exists in system but not Excel:")
        for e in extra_items:
            print(f" - {e}")
    else:
        print("\n✅ No extra items")

    print("\n✔ Analysis complete")

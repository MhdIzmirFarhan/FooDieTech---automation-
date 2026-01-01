from playwright.sync_api import sync_playwright
import pandas as pd
from main import login
import config

def analyze_items_by_id(file_path, max_id):
    BASE_URL = f"https://{config.restaurant}.foodiee.com.my/itemmanage/item_food/create"

    # -----------------------------
    # READ EXCEL
    # -----------------------------
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    required_cols = {"food", "price"}
    if not required_cols.issubset(df.columns):
        print("❌ Excel must contain: food, price")
        return

    excel_items = {
        str(row.food).strip(): str(row.price).strip()
        for row in df.itertuples(index=False)
    }

    system_items = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=80)
        context = browser.new_context()
        page = context.new_page()

        # LOGIN
        login(page, email="admin@gmail.com", password="FooDiee#25!")

        # -----------------------------
        # LOOP THROUGH IDS
        # -----------------------------
        for item_id in range(1, max_id + 1):
            url = f"{BASE_URL}/{item_id}"
            page.goto(url, timeout=60000)

            try:
                page.wait_for_selector("input[name='foodname']", timeout=5000)
            except:
                continue  # page not valid

            food = page.locator("input[name='foodname']").input_value().strip()
            price = page.locator("input[name='foodprice']").input_value().strip()

            if not food:
                continue  # empty / deleted item

            system_items[food] = price

        browser.close()

    # -----------------------------
    # COMPARISON
    # -----------------------------
    missing_items = []
    wrong_items = []

    for name, price in excel_items.items():
        if name not in system_items:
            missing_items.append(name)
        elif system_items[name] != price:
            wrong_items.append(
                f"{name} | Excel: {price} | System: {system_items[name]}"
            )

    extra_items = [
        name for name in system_items if name not in excel_items
    ]

    # -----------------------------
    # REPORT
    # -----------------------------
    print("\n📊 ANALYSIS REPORT (BY ID)")
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

    print("\n✔ Deep analysis complete")

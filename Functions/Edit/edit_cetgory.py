from playwright.sync_api import sync_playwright
import pandas as pd
import time
from main import login
import config


def edit_categories_from_excel(file_path):
    CATEGORY_URL = f"https://{config.restaurant}.foodiee.com.my/itemmanage/item_category"

    # -----------------------------
    # READ EXCEL (sheet = edit)
    # -----------------------------
    try:
        df = pd.read_excel(file_path, sheet_name="edit")
    except ValueError:
        print("❌ Sheet 'edit' not found")
        return

    required_cols = {
        "ref_category",
        "category_name",
        "parent_category",
        "status",
        "is_web",
        "is_open_item"
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

        login(page, "admin@gmail.com", "FooDiee#25!")

        page.goto(CATEGORY_URL, timeout=60000)
        page.wait_for_selector("input[type='search']", timeout=60000)

        # -----------------------------
        # LOOP EXCEL
        # -----------------------------
        for _, row in df.iterrows():

            ref_category = str(row["ref_category"]).strip()
            category_name = str(row["category_name"]).strip()

            # skip rows not meant for category edit
            if not ref_category:
                continue

            parent_category = str(row["parent_category"]).strip()
            status = str(row["status"]).strip()
            is_web = str(row["is_web"]).strip()
            is_open_item = str(row["is_open_item"]).strip()

            print(f"\n✏️ Editing category: {ref_category} → {category_name}")

            # SEARCH CATEGORY
            search_box = page.locator("input[type='search']")
            search_box.fill("")
            search_box.fill(ref_category)
            time.sleep(1)

            rows = page.locator("#DataTables_Table_0 tbody tr")

            if rows.count() == 0:
                print(f"❌ Category not found: {ref_category}")
                continue

            # CLICK UPDATE
            rows.first.locator("a[title='Update']").click()

            page.wait_for_selector("input[name='categoryname']", timeout=10000)

            # -----------------------------
            # CATEGORY NAME
            # -----------------------------
            if category_name:
                page.fill("input[name='categoryname']", category_name)

            # -----------------------------
            # PARENT CATEGORY
            # -----------------------------
            if parent_category:
                page.select_option(
                    "select[name='Parentcategory']",
                    label=parent_category
                )
            else:
                page.select_option("select[name='Parentcategory']", "")

            # -----------------------------
            # STATUS
            # -----------------------------
            page.select_option(
                "select[name='status']",
                "1" if status.lower() == "active" else "0"
            )

            # -----------------------------
            # WEB STATUS
            # -----------------------------
            page.select_option(
                "select[name='is_web']",
                "1" if is_web.lower() == "active" else "0"
            )

            # -----------------------------
            # OPEN ITEM
            # -----------------------------
            open_item_checkbox = page.locator("#is_open_item")
            should_be_checked = is_open_item.lower() == "yes"

            if open_item_checkbox.is_checked() != should_be_checked:
                open_item_checkbox.click()

            # -----------------------------
            # SAVE
            # -----------------------------
            page.click("button[type='submit']")
            print(f"✅ Updated: {category_name or ref_category}")

            time.sleep(2)

            page.goto(CATEGORY_URL)
            page.wait_for_selector("input[type='search']", timeout=60000)

        print("\n🎉 All categories processed")
        input("Press Enter to close browser...")
        browser.close()


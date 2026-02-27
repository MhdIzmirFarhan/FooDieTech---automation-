from playwright.sync_api import sync_playwright
import pandas as pd
import time
import os
from main import login, get_current_item_data
import config


def edit_items_from_excel(file_path, max_extra_notes=3):
    ITEM_LIST_URL = f"https://{config.restaurant}.foodiee.com.my/itemmanage/item_food"

    # -----------------------------
    # READ EXCEL (sheet = edit)
    # -----------------------------
    try:
        df = pd.read_excel(file_path, sheet_name="edit")
    except ValueError:
        print("❌ Sheet 'edit' not found")
        return

    required_cols = {
        "ref_food_name",
        "food",
        "tamil",
        "price",
        "category",
        "kitchen",
        "sessions",
        "extra_notes",
        "max_extra_notes_limit"
    }

    if not required_cols.issubset(df.columns):
        print("❌ Excel missing required columns")
        return

    # -----------------------------
    # SEARCH + OPEN ITEM
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
            print(f"❌ Item not found: {food_name}")
            return False

        rows.first.locator("a").first.click()
        page.wait_for_selector("input[name='foodname']", timeout=60000)
        return True

    # -----------------------------
    # PLAYWRIGHT
    # -----------------------------
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=80)
        context = browser.new_context()
        page = context.new_page()

        login(page, email="admin@gmail.com", password="FooDiee#25!")

        for _, row in df.iterrows():

            ref_food = str(row["ref_food_name"]).strip()
            new_food = str(row["food"]).strip()

            print(f"\n✏️ Editing: {ref_food} → {new_food}")

            if not search_and_open(page, ref_food):
                continue

            # -----------------------------
            # CLEAN HELPER
            # -----------------------------
            def clean(val):
                if pd.isna(val):
                    return ""
                val = str(val).strip()
                return "" if val.lower() == "nan" else val

            price = clean(row["price"])
            category = clean(row["category"])
            kitchen = clean(row["kitchen"])
            sessions = clean(row["sessions"])
            extra_notes_raw = clean(row["extra_notes"])
            image_name = clean(row.get("img", ""))

            food_tamil = clean(row.get("tamil", ""))
            max_limit = row.get("max_extra_notes_limit")
            max_limit = max_extra_notes if pd.isna(max_limit) else int(max_limit)

            # -----------------------------
            # CURRENT DATA
            # -----------------------------
            current = get_current_item_data(page)

            def same(field, excel_val):
                return excel_val and str(current.get(field)) == excel_val

            # -----------------------------
            # FOOD NAME (NEW)
            # -----------------------------
            if new_food and not same("food", new_food):
                page.fill("input[name='foodname']", new_food)

            # -----------------------------
            # FOOD TAMIL NAME
            # -----------------------------
            if food_tamil and not same("tamil", food_tamil):
                page.fill("input[name='foodnametn']", food_tamil)

            # -----------------------------
            # CATEGORY
            # -----------------------------
            if category and not same("category", category):
                page.click("select[name='CategoryID'] + span.select2")
                page.locator(".select2-results__option", has_text=category).first.click()

            # -----------------------------
            # KITCHEN
            # -----------------------------
            if kitchen and not same("kitchen", kitchen):
                page.click("select[name='kitchen'] + span.select2")
                page.locator(".select2-results__option", has_text=kitchen).first.click()

            # -----------------------------
            # PRICE
            # -----------------------------
            if price and not same("price", price):
                page.fill("input[name='foodprice']", price)

            # -----------------------------
            # SESSIONS
            # -----------------------------
            if sessions:
                for s in sessions.split(","):
                    s = s.strip()
                    if not s:
                        continue

                    page.click("select[name='food_sessions[]'] + span.select2")
                    search = page.locator(".select2-container--open input.select2-search__field")
                    search.fill(s)

                    page.wait_for_selector(".select2-results__option", timeout=5000)
                    page.locator(".select2-results__option", has_text=s).first.click()
                    time.sleep(0.2)

                page.keyboard.press("Escape")

            # -----------------------------
            # EXTRA NOTES (SAME AS SESSIONS)
            # -----------------------------
            if pd.isna(extra_notes_raw):
                extra_notes_raw = ""
            else:
                extra_notes_raw = str(extra_notes_raw).strip()
            
            if extra_notes_raw:
                # Set max limit
                page.fill("input[name='extra_notes_limit']", str(max_limit))
            
                notes = [
                    n.strip()
                    for n in extra_notes_raw.split(",")
                    if n.strip().lower() != "nan"
                ][:max_limit]
            
                for note in notes:
                    note = note.strip()
                    if not note:
                        continue
            
                    # Open Extra Notes Select2
                    page.click("select#extra_notes + span.select2")
            
                    # Scope search to THIS open Select2 only
                    search = page.locator(
                        ".select2-container--open .select2-search__field"
                    )
            
                    search.fill(note)
            
                    # Wait for dropdown results
                    page.wait_for_selector(
                        ".select2-results__option",
                        timeout=5000
                    )
            
                    # Click matching option
                    page.locator(
                        ".select2-results__option",
                        has_text=note
                    ).first.click()
            
                    time.sleep(0.2)
            
                # Close dropdown
                page.keyboard.press("Escape")           

            # -----------------------------
            # STATUS
            # -----------------------------
            page.select_option("select[name='status']", "1")

            # -----------------------------
            # SAVE
            # -----------------------------
            page.click("button[type='submit']")
            print("✅ Updated")
            time.sleep(2)

        print("\n🎉 All items processed")
        input("Press Enter to close...")
        browser.close()


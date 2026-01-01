# from playwright.sync_api import sync_playwright
# import pandas as pd
# import time
# import os
# from main import restaurant, login, get_current_item_data


# def edit_items_from_excel(file_path, max_extra_notes=3):
#     ITEM_LIST_URL = f"https://{restaurant}.foodiee.com.my/itemmanage/item_food"

#     # -----------------------------
#     # READ EXCEL
#     # -----------------------------
#     df = pd.read_csv(file_path) if file_path.endswith(".csv") else pd.read_excel(file_path)

#     required_cols = {
#         "food", "price", "category", "kitchen",
#         "sessions", "extra notes", "max extra notes limit"
#     }

#     if not required_cols.issubset(df.columns):
#         print("❌ Excel missing required columns")
#         return

#     # -----------------------------
#     # HELPER: SEARCH + OPEN ITEM
#     # -----------------------------
#     def search_and_open(page, food_name):
#         page.goto(ITEM_LIST_URL, timeout=60000)

#         search_box = page.locator("#DataTables_Table_0_filter input[type='search']")
#         search_box.wait_for(state="visible", timeout=10000)

#         search_box.fill("")
#         search_box.fill(food_name)
#         time.sleep(1)

#         rows = page.locator("tbody tr")
#         if rows.count() == 0:
#             print(f"❌ Item not found: {food_name}")
#             return False

#         rows.first.locator("a").first.click()
#         page.wait_for_selector("input[name='foodname']", timeout=60000)
#         return True

#     # -----------------------------
#     # PLAYWRIGHT
#     # -----------------------------
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False, slow_mo=80)
#         context = browser.new_context()
#         page = context.new_page()

#         login(page, email="admin@gmail.com", password="FooDiee#25!")

#         for _, row in df.iterrows():
#             food = str(row["food"]).strip()
#             print(f"\n✏️ Editing: {food}")

#             if not search_and_open(page, food):
#                 continue

#             # -----------------------------
#             # CLEAN EXCEL VALUES
#             # -----------------------------
#             def clean(val):
#                 return "" if pd.isna(val) else str(val).strip()

#             price = clean(row["price"])
#             category = clean(row["category"])
#             kitchen = clean(row["kitchen"])
#             sessions = clean(row["sessions"])
#             extra_notes_raw = clean(row["extra notes"])
#             image_name = str(row.get("img", "")).strip()

#             max_limit = row.get("max extra notes limit")
#             max_limit = max_extra_notes if pd.isna(max_limit) else int(max_limit)

#             # -----------------------------
#             # CURRENT DATA
#             # -----------------------------
#             current = get_current_item_data(page)

#             def same(field, excel_val):
#                 return excel_val and str(current.get(field)) == excel_val

#             # -----------------------------
#             # CATEGORY
#             # -----------------------------
#             if category and not same("category", category):
#                 page.click("select[name='CategoryID'] + span.select2")
#                 page.locator(".select2-results__option", has_text=category).first.click()

#             # -----------------------------
#             # KITCHEN
#             # -----------------------------
#             if kitchen and not same("kitchen", kitchen):
#                 page.click("select[name='kitchen'] + span.select2")
#                 page.locator(".select2-results__option", has_text=kitchen).first.click()

#             # -----------------------------
#             # PRICE
#             # -----------------------------
#             if price and not same("price", price):
#                 page.fill("input[name='foodprice']", price)

#             # -----------------------------
#             # FOOD SESSIONS
#             # -----------------------------
#             if sessions:
#                 for s in sessions.split(","):
#                     s = s.strip()
#                     if not s:
#                         continue

#                     page.click("select[name='food_sessions[]'] + span.select2")
#                     search = page.locator(".select2-container--open input.select2-search__field")
#                     search.fill(s)

#                     page.wait_for_selector(".select2-results__option", timeout=5000)
#                     page.locator(".select2-results__option", has_text=s).first.click()
#                     time.sleep(0.2)

#                 page.keyboard.press("Escape")

#             # -----------------------------
#             # EXTRA NOTES
#             # -----------------------------
#             if extra_notes_raw:
#                 page.fill("input[name='extra_notes_limit']", str(max_limit))

#                 notes = [
#                     n.strip()
#                     for n in extra_notes_raw.split(",")
#                     if n.strip().lower() != "nan"
#                 ][:max_limit]

#                 for note in notes:
#                     page.click("#extra_notes + span.select2")
#                     search = page.locator(".select2-container--open input.select2-search__field")
#                     search.fill(note)

#                     page.wait_for_selector(".select2-results__option", timeout=5000)
#                     page.locator(".select2-results__option", has_text=note).first.click()
#                     time.sleep(0.2)

#                 page.keyboard.press("Escape")

#             # -----------------------------
#             # IMAGE UPLOAD (CORRECT WAY)
#             # -----------------------------
#             if image_name:
#                 foods = r"C:\Users\User\Videos\foodimages\Foods"
#                 beverages = r"C:\Users\User\Videos\foodimages\Beverages"

#                 img_path = os.path.join(foods, image_name)
#                 if not os.path.exists(img_path):
#                     img_path = os.path.join(beverages, image_name)

#                 if os.path.exists(img_path):
#                     page.set_input_files("input[name='picture']", img_path)
#                     time.sleep(1)
#                 else:
#                     print(f"⚠️ Image not found: {image_name}")
            

#             # -----------------------------
#             # STATUS
#             # -----------------------------
#             page.select_option("select[name='status']", "1")

#             # -----------------------------
#             # SAVE
#             # -----------------------------
#             page.click("button[type='submit']")
#             print("✅ Updated")
#             time.sleep(2)

#         print("\n🎉 All items processed")
#         input("Press Enter to close...")
#         browser.close()

from playwright.sync_api import sync_playwright
import pandas as pd
import time
import os
from main import login, get_current_item_data
import config


def edit_items_from_excel(file_path, max_extra_notes=3):
    ITEM_LIST_URL = f"https://{config.restaurant}.foodiee.com.my/itemmanage/item_food"

    # -----------------------------
    # READ EXCEL / CSV
    # -----------------------------
    df = pd.read_csv(file_path) if file_path.endswith(".csv") else pd.read_excel(file_path)

    required_cols = {
        "food", "price", "category", "kitchen",
        "sessions", "extra notes", "max extra notes limit"
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
            food = str(row["food"]).strip()
            print(f"\n✏️ Editing: {food}")

            if not search_and_open(page, food):
                continue

            # -----------------------------
            # CLEAN VALUES
            # -----------------------------
            def clean(val):
                return "" if pd.isna(val) else str(val).strip()

            price = clean(row["price"])
            category = clean(row["category"])
            kitchen = clean(row["kitchen"])
            sessions = clean(row["sessions"])
            extra_notes_raw = clean(row["extra notes"])
            image_name = clean(row.get("img", ""))

            max_limit = row.get("max extra notes limit")
            max_limit = max_extra_notes if pd.isna(max_limit) else int(max_limit)

            # -----------------------------
            # CURRENT DATA (TEXT ONLY)
            # -----------------------------
            current = get_current_item_data(page)

            def same(field, excel_val):
                return excel_val and str(current.get(field)) == excel_val

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
            # FOOD SESSIONS
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
            # EXTRA NOTES
            # -----------------------------
            if extra_notes_raw:
                page.fill("input[name='extra_notes_limit']", str(max_limit))

                notes = [
                    n.strip()
                    for n in extra_notes_raw.split(",")
                    if n.strip().lower() != "nan"
                ][:max_limit]

                for note in notes:
                    page.click("#extra_notes + span.select2")
                    search = page.locator(".select2-container--open input.select2-search__field")
                    search.fill(note)

                    page.wait_for_selector(".select2-results__option", timeout=5000)
                    page.locator(".select2-results__option", has_text=note).first.click()
                    time.sleep(0.2)

                page.keyboard.press("Escape")

            # -----------------------------
            # IMAGE UPLOAD (EDIT MODE – FORCE)
            # -----------------------------
            if image_name and image_name.lower() != "nan":
                foods = r"C:\Users\User\Videos\foodimages\Foods"
                beverages = r"C:\Users\User\Videos\foodimages\Beverages"

                img_path = os.path.join(foods, image_name)
                if not os.path.exists(img_path):
                    img_path = os.path.join(beverages, image_name)

                if os.path.exists(img_path):
                    print(f"🖼 Updating image: {image_name}")

                    file_input = page.locator("input[name='picture']")
                    file_input.set_input_files(img_path)

                    # 🔥 trigger onchange (VERY IMPORTANT)
                    page.evaluate("""
                        const input = document.querySelector("input[name='picture']");
                        input.dispatchEvent(new Event('change', { bubbles: true }));
                    """)

                    time.sleep(1.5)
                else:
                    print(f"⚠️ Image not found: {image_name}")

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

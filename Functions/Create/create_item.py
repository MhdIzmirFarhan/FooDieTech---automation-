from playwright.sync_api import sync_playwright
import pandas as pd
import time
import os
from main import login
import config

def create_items(file_path, max_extra_notes=3):
    URL = f"https://{config.restaurant}.foodiee.com.my/itemmanage/item_food/create"
    ASSIGN_URL = f"https://{config.restaurant}.foodiee.com.my/itemmanage/menu_addons/assignaddons"

    # -----------------------------
    # READ EXCEL / CSV
    # -----------------------------
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    required_cols = {
        "food", "price", "category", "kitchen",
        "sessions", "extra notes", "max extra notes limit"
    }

    if not required_cols.issubset(df.columns):
        print("❌ Excel missing required columns:", required_cols)
        return

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
        # LOOP ITEMS
        # -----------------------------
        for _, row in df.iterrows():
            food = str(row["food"]).strip()
            price = str(row["price"]).strip()
            category = str(row["category"]).strip()
            kitchen = str(row["kitchen"]).strip()
            sessions = str(row["sessions"]).strip()
            add_ons = str(row.get("add_ons", "")).strip()
            image_name = str(row.get("img", "")).strip()

            extra_notes_raw = str(row.get("extra notes", "")).strip()
            max_limit = row.get("max extra notes limit", max_extra_notes)

            if pd.isna(max_limit) or str(max_limit).strip() == "":
                max_limit = max_extra_notes
            else:
                max_limit = int(max_limit)

            # -----------------------------
            # OPEN CREATE PAGE
            # -----------------------------
            page.goto(URL, timeout=60000)
            page.wait_for_selector("select[name='CategoryID']", timeout=60000)

            # Category
            page.click("select[name='CategoryID'] + span.select2")
            page.locator(".select2-results__option", has_text=category).first.click()

            # Kitchen
            page.click("select[name='kitchen'] + span.select2")
            page.locator(".select2-results__option", has_text=kitchen).first.click()

            # Name & Price
            page.fill("input[name='foodname']", food)
            page.fill("input[name='foodprice']", price)

            # -----------------------------
            # IMAGE UPLOAD
            # -----------------------------
            if image_name:
                foods = r"C:\Users\User\Videos\foodimages\Foods"
                beverages = r"C:\Users\User\Videos\foodimages\Beverages"

                img_path = os.path.join(foods, image_name)
                if not os.path.exists(img_path):
                    img_path = os.path.join(beverages, image_name)

                if os.path.exists(img_path):
                    page.set_input_files("input[name='picture']", img_path)
                    time.sleep(1)
                else:
                    print(f"⚠️ Image not found: {image_name}")

            # -----------------------------
            # FOOD SESSIONS
            # -----------------------------
            for s in sessions.split(","):
                s = s.strip()
                if not s:
                    continue

                page.click("select[name='food_sessions[]'] + span.select2")
                search = page.locator(".select2-container--open .select2-search__field")
                search.fill(s)
                page.wait_for_selector(".select2-results__option", timeout=5000)
                page.locator(".select2-results__option", has_text=s).first.click()
                time.sleep(0.2)

            page.keyboard.press("Escape")

            # -----------------------------
            # CLEAN EXCEL VALUE
            # -----------------------------
            if pd.isna(extra_notes_raw):
                extra_notes_raw = ""
            else:
                extra_notes_raw = str(extra_notes_raw).strip()
            
            if extra_notes_raw:
                page.fill("input[name='extra_notes_limit']", str(max_limit))
            
                notes = [
                    n.strip()
                    for n in extra_notes_raw.split(",")
                    if n.strip().lower() != "nan"
                ][:max_limit]
            
                for note in notes:
                    page.click("#extra_notes + span.select2")
            
                    search = page.locator(
                        ".select2-container--open input.select2-search__field"
                    )
                    search.wait_for(state="visible", timeout=5000)
            
                    search.fill(note)
            
                    page.wait_for_selector(".select2-results__option", timeout=5000)
                    page.locator(
                        ".select2-results__option",
                        has_text=note
                    ).first.click()
            
                    time.sleep(0.2)
            
                page.keyboard.press("Escape")
            

            # -----------------------------
            # STATUS
            # -----------------------------
            page.select_option("select[name='status']", "1")

            # SAVE
            page.click("button[type='submit']")
            print(f"✅ Created food: {food}")
            time.sleep(2)

            # -----------------------------
            # ADD-ONS (OPTIONAL → SKIP IF EMPTY)
            # -----------------------------
            if not add_ons or str(add_ons).strip().lower() in ("", "nan"):
                print(f"⏭️ No add-ons for: {food} → skipping")
                continue  # move to NEXT ITEM immediately
            
            addon_list = [a.strip() for a in add_ons.split(",") if a.strip()]
            
            if not addon_list:
                print(f"⏭️ Add-ons empty after parsing for: {food}")
                continue
            
            # Only reach here IF add-ons exist
            page.goto(ASSIGN_URL, timeout=60000)
            page.click("button[data-target='#add0']")
            page.wait_for_selector("select[name='addonsid']", timeout=60000)
            
            # Select add-ons
            page.click("select[name='addonsid'] + span.select2")
            for addon in addon_list:
                search = page.locator(".select2-container--open .select2-search__field")
                search.fill(addon)
                time.sleep(0.3)
                page.locator(
                    ".select2-results__option",
                    has_text=addon
                ).first.click()
            
            # Select food
            page.click("select[name='menuid'] + span.select2")
            search = page.locator(".select2-container--open .select2-search__field")
            search.fill(food)
            time.sleep(0.5)
            page.locator(
                ".select2-results__option",
                has_text=food
            ).first.click()
            
            page.click("button[type='submit']")
            print(f"➕ Add-ons assigned: {food}")
            time.sleep(2)
            

        browser.close()

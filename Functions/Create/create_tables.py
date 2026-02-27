from playwright.sync_api import sync_playwright
from main import login   # your existing login helper
import time
import pandas as pd
import config


def create_tables_from_excel(excel_path):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=80)
        context = browser.new_context()
        page = context.new_page()

        login(page, "admin@gmail.com", "FooDiee#25!")

        page.goto(
            f"https://{config.restaurant}.foodiee.com.my/setting/restauranttable/create",
            wait_until="networkidle"
        )

        df = pd.read_excel(excel_path, sheet_name="Table")

        for _, row in df.iterrows():
            # your existing logic here
            table_name = str(row["table_name"]).strip()
            capacity = str(row["capacity"]).strip()
            floor_name = str(row["floor"]).strip()
            image_name = str(row["image"]).strip()
    
            # ---------------- 1. CLICK ADD TABLE ----------------
            page.click("button:has-text('Add Table')")
            page.wait_for_selector("#tablename", timeout=5000)
    
            # ---------------- 2. TABLE NAME ----------------
            page.fill("#tablename", table_name)
    
            # ---------------- 3. CAPACITY ----------------
            if capacity.lower() != "nan":
                page.fill("#capacity", capacity)
    
            # ---------------- 4. FLOOR (SELECT2) ----------------
            page.click("#select2-floor-container")
    
            search_input = page.locator(
                ".select2-container--open .select2-search__field"
            )
            search_input.wait_for(state="visible", timeout=5000)
            search_input.fill(floor_name)
            search_input.press("Enter")
    
            time.sleep(0.3)
    
            # ---------------- 5. SHOW IMAGE MODAL ----------------
            page.click("button:has-text('Show')")
            page.wait_for_selector("#newtable img", timeout=5000)
    
            # ---------------- 6. SELECT IMAGE ----------------
            page.locator(
                f"#newtable img[data-scr*='{image_name}']"
            ).first.click()
    
            time.sleep(0.3)
    
            # ---------------- 7. SUBMIT ----------------
            page.click("button[type='submit']:has-text('Add')")
    
            time.sleep(1)
        
            print("✅ Tables created successfully")
            pass

        browser.close()

    # ---------------- 0. OPEN TABLE CREATE PAGE ----------------

    

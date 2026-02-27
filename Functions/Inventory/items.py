from playwright.sync_api import sync_playwright
import pandas as pd
import time
import os
from main import login
import config


def create_inventory_items(file_path):
    URL = f"https://{config.restaurant}.foodiee.com.my/inventory/items/create"

    # -----------------------------
    # READ FILE
    # -----------------------------
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

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
            item_name = str(row.get("item_name", "")).strip()
            if not item_name:
                print("⏭️ Skipped empty item")
                continue

            print(f"➕ Creating item: {item_name}")

            page.goto(URL, timeout=60000)
            page.wait_for_selector("input[name='item_name']", timeout=60000)

            # -----------------------------
            # ITEM CODE (auto-generated)
            # -----------------------------
            item_code = str(row.get("item_code", "")).strip()
            if item_code:
                # Click edit code if a manual code is provided
                page.click("#editCode")
                page.fill("input[name='item_code']", item_code)

            # -----------------------------
            # ITEM NAME
            # -----------------------------
            page.fill("input[name='item_name']", item_name)

            # -----------------------------
            # ITEM TYPE (Select2)
            # -----------------------------
            item_type = str(row.get("item_type", "ingredient")).strip()
            if item_type:
                page.click("select[name='item_type'] + span.select2")
                page.locator(".select2-results__option", has_text=item_type.capitalize()).first.click()

            # -----------------------------
            # CATEGORY (Select2)
            # -----------------------------
            category = str(row.get("category", "")).strip()
            if category:
                page.click("select[name='category_id'] + span.select2")
                page.locator(".select2-results__option", has_text=category).first.click()

            # -----------------------------
            # DESCRIPTION
            # -----------------------------
            description = str(row.get("description", "")).strip()
            if description:
                page.fill("textarea[name='description']", description)

            # -----------------------------
            # BARCODE
            # -----------------------------
            barcode = str(row.get("barcode", "")).strip()
            if barcode:
                page.fill("input[name='barcode']", barcode)

            # -----------------------------
            # BRAND
            # -----------------------------
            brand = str(row.get("brand", "")).strip()
            if brand:
                page.fill("input[name='brand']", brand)

            # -----------------------------
            # MODEL
            # -----------------------------
            model = str(row.get("model", "")).strip()
            if model:
                page.fill("input[name='model']", model)

            # -----------------------------
            # IMAGE UPLOAD
            # -----------------------------
            # image = str(row.get("image", "")).strip()
            # if image and image.lower() != "nan":
            #     img_path = os.path.join(config.IMAGE_DIR, image)
            #     if os.path.exists(img_path):
            #         page.set_input_files("input[name='item_image']", img_path)
            #         time.sleep(1)
            #     else:
            #         print(f"⚠️ Image not found, skipped: {image}")

            # -----------------------------
            # UNIT OF MEASURE (Select2)
            # -----------------------------
            uom = str(row.get("uom", "")).strip()
            
            if uom and uom.lower() != "nan":
                # Open the Select2 dropdown
                page.click("select[name='uom_id'] + span.select2")
            
                # Wait for the Select2 search input to appear
                search_box = page.wait_for_selector(
                    ".select2-container--open input.select2-search__field",
                    timeout=5000
                )
            
                # Type the UOM value (e.g. KG, GM, PCS)
                search_box.fill(uom)
            
                # Press Enter to select the highlighted option
                search_box.press("Enter")
            
            
            # -----------------------------
            # PURCHASE UNIT (Select2)
            # -----------------------------
            purchase_uom = str(row.get("purchase_uom", "")).strip()
            if purchase_uom and purchase_uom.lower() != "nan":
                # Open the Select2 dropdown
                page.click("select[name='uom_id'] + span.select2")
            
                # Wait for the Select2 search input to appear
                search_box = page.wait_for_selector(
                    ".select2-container--open input.select2-search__field",
                    timeout=5000
                )
            
                # Type the UOM value (e.g. KG, GM, PCS)
                search_box.fill(uom)
            
                # Press Enter to select the highlighted option
                search_box.press("Enter")
            
            # -----------------------------
            # CONVERSION RATIO
            # -----------------------------
            conversion_ratio = str(row.get("conversion_ratio", "")).strip()
            if conversion_ratio and conversion_ratio.lower() != "nan":
                page.fill(
                    "input[name='conversion_ratio']",
                    conversion_ratio
                )
            
            # -----------------------------
            # STOCK MANAGEMENT
            # -----------------------------
            min_stock = str(row.get("min_stock", "")).strip()
            if min_stock and min_stock.lower() != "nan":
                page.fill("input[name='min_stock_level']", min_stock)
            
            max_stock = str(row.get("max_stock", "")).strip()
            if max_stock and max_stock.lower() != "nan":
                page.fill("input[name='max_stock_level']", max_stock)
            
            reorder_level = str(row.get("reorder_level", "")).strip()
            if reorder_level and reorder_level.lower() != "nan":
                page.fill("input[name='reorder_level']", reorder_level)
            
            # -----------------------------
            # DEFAULT LOCATION (Select2)
            # -----------------------------
            location = str(row.get("location", "")).strip()
            if location and location.lower() != "nan":
                page.click("select[name='default_location_id'] + span.select2")
                page.locator(
                    ".select2-results__option",
                    has_text=location
                ).first.click()
            
            # -----------------------------
            # SHELF LIFE
            # -----------------------------
            shelf_life = str(row.get("shelf_life", "")).strip()
            if shelf_life and shelf_life.lower() != "nan":
                page.fill("input[name='shelf_life_days']", shelf_life)
            
            # -----------------------------
            # STORAGE TEMPERATURE
            # -----------------------------
            storage_temp = str(row.get("storage_temperature", "")).strip()
            if storage_temp and storage_temp.lower() != "nan":
                page.select_option(
                    "select[name='storage_temperature']",
                    storage_temp
                )

            # -----------------------------
            # SUBMIT FORM (Save Item)
            # -----------------------------
            page.locator("button:has-text('Save Item')").click()


        browser.close()

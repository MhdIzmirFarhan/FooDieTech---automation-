from playwright.sync_api import sync_playwright
import pandas as pd
import time
import os
from main import login
import config

def create_categories_from_excel(file_path):
    URL = f"https://{config.restaurant}.foodiee.com.my/itemmanage/item_category/create"

    # -----------------------------
    # READ EXCEL / CSV
    # -----------------------------
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path, sheet_name="Category")


    required_cols = {"category_name"}

    if not required_cols.issubset(df.columns):
        print("❌ Excel must contain column: category_name")
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

        # -----------------------------
        # LOOP CATEGORIES
        # -----------------------------
        for _, row in df.iterrows():

            # CLEAN VALUES
            category_name = "" if pd.isna(row["category_name"]) else str(row["category_name"]).strip()
            image_name = "" if pd.isna(row.get("image")) else str(row.get("image")).strip()

            if not category_name:
                print("⏭️ Empty category name → skipping")
                continue

            print(f"\n➕ Creating category: {category_name}")

            # -----------------------------
            # OPEN CREATE PAGE
            # -----------------------------
            page.goto(URL, timeout=60000)
            page.wait_for_selector("input[name='categoryname']", timeout=60000)

            # -----------------------------
            # CATEGORY NAME
            # -----------------------------
            page.fill("input[name='categoryname']", category_name)

            # -----------------------------
            # IMAGE UPLOAD (OPTIONAL)
            # -----------------------------
            if image_name:
                category_images = r"C:\Users\User\Videos\foodimages\Categories"

                img_path = os.path.join(category_images, image_name)

                if os.path.exists(img_path):
                    page.set_input_files("input[name='picture']", img_path)
                    time.sleep(1)
                else:
                    print(f"⚠️ Image not found: {image_name}")

            # -----------------------------
            # SAVE
            # -----------------------------
            page.click("button[type='submit']")
            print(f"✅ Category created: {category_name}")
            time.sleep(2)

        print("\n🎉 All categories processed")
        input("Press Enter to close browser...")
        browser.close()

# from playwright.sync_api import sync_playwright
# import pandas as pd
# import time
# import os
# from main import restaurant

# def add_addons(file_path):
#     URL = f"https://{restaurant}.foodiee.com.my/itemmanage/menu_addons/create"

#     # -----------------------------
#     # READ 'add_on' SHEET
#     # -----------------------------
#     df = pd.read_excel(file_path, sheet_name="add_on")

#     # -----------------------------
#     # PLAYWRIGHT
#     # -----------------------------
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False, slow_mo=80)
#         context = browser.new_context()
#         page = context.new_page()

#         page.goto(URL, timeout=60000)
#         print("👉 Login & solve captcha manually")
#         input("Press ENTER after login is completed...")

#         for _, row in df.iterrows():
#             name = str(row.get("Add-ons Name", ""))
#             price = str(row.get("Price", "0"))
#             status = str(row.get("Status", "1"))  # Default Active

#             page.goto(URL, timeout=60000)
#             page.wait_for_selector("input#addonsname", timeout=60000)

#             # -----------------------------
#             # ADD-ON NAME & PRICE
#             # -----------------------------
#             page.fill("input#addonsname", name)
#             page.fill("input#addonsprice", price)

#             # -----------------------------
#             # STATUS SELECT
#             # -----------------------------
#             page.select_option("select[name='status']", status)

#             # -----------------------------
#             # SUBMIT
#             # -----------------------------
#             page.click("button[type='submit']")
#             print(f"✅ Add-on submitted: {name}")

#             time.sleep(2)

#         browser.close()

from playwright.sync_api import sync_playwright
import pandas as pd
import time
from main import login
import config


def add_addons(file_path):
    URL = f"https://{config.restaurant}.foodiee.com.my/itemmanage/menu_addons/create"

    # -----------------------------
    # READ 'add_on' SHEET
    # -----------------------------
    df = pd.read_excel(file_path, sheet_name="Add-ons")

    # -----------------------------
    # PLAYWRIGHT
    # -----------------------------
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=80)
        context = browser.new_context()
        page = context.new_page()

        # -----------------------------
        # AUTO LOGIN (LIKE OTHER SCRIPTS)
        # -----------------------------
        login(
            page,
            email="admin@gmail.com",
            password="FooDiee#25!"
        )

        # -----------------------------
        # GO TO ADD-ON PAGE
        # -----------------------------
        page.goto(URL, timeout=60000)

        print("🧩 Please solve the captcha manually.")
        input("➡️ Press ENTER once captcha is completed...")

        # -----------------------------
        # LOOP ADD-ONS
        # -----------------------------
        for _, row in df.iterrows():
            name = str(row.get("add_ons_name", "")).strip()
            price = str(row.get("price", "0")).strip()
            status = str(row.get("status", "1")).strip()  # Default Active

            if not name:
                print("⚠️ Skipping empty add-on name")
                continue

            page.goto(URL, timeout=60000)
            page.wait_for_selector("input#addonsname", timeout=60000)

            # -----------------------------
            # ADD-ON NAME & PRICE
            # -----------------------------
            page.fill("input#addonsname", name)
            page.fill("input#addonsprice", price)

            # -----------------------------
            # STATUS
            # -----------------------------
            page.select_option("select[name='status']", status)

            # -----------------------------
            # SUBMIT
            # -----------------------------
            page.click("button[type='submit']")
            print(f"✅ Add-on submitted: {name}")

            time.sleep(2)

        print("\n🎉 All add-ons processed")
        browser.close()


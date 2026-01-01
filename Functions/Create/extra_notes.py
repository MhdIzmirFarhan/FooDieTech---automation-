from playwright.sync_api import sync_playwright
import pandas as pd
import time
from main import login
import config

def create_extra_notes_from_excel(file_path):
    URL = f"https://{config.restaurant}.foodiee.com.my/itemmanage/extra_notes/create"

    # -----------------------------
    # READ EXCEL / CSV
    # -----------------------------
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path, sheet_name="extra_notes")


    if "note_name" not in df.columns:
        print("❌ Excel must contain column: note_name")
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
        # LOOP EXTRA NOTES
        # -----------------------------
        for _, row in df.iterrows():

            note_name = "" if pd.isna(row["note_name"]) else str(row["note_name"]).strip()

            if not note_name:
                print("⏭️ Empty / NaN note → skipping")
                continue

            print(f"➕ Creating extra note: {note_name}")

            # OPEN CREATE PAGE
            page.goto(URL, timeout=60000)

            # WAIT FOR INPUT
            page.wait_for_selector("input[name='note_name']", timeout=60000)

            # FILL NOTE NAME
            page.fill("input[name='note_name']", note_name)

            # SUBMIT
            page.click("button[type='submit']")

            print(f"✅ Extra note created: {note_name}")
            time.sleep(1.5)

        print("\n🎉 All extra notes processed")
        input("Press Enter to close browser...")
        browser.close()

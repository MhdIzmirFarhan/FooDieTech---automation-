from playwright.sync_api import sync_playwright
import pandas as pd
import time
from main import login
import config

def create_sessions_from_excel(file_path):
    URL = f"https://{config.restaurant}.foodiee.com.my/itemmanage/session_master/create"

    # -----------------------------
    # READ EXCEL / CSV
    # -----------------------------
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    else:
        # Read specifically from sheet named "session"
        df = pd.read_excel(file_path, sheet_name="Sessions")

    required_cols = {
        "session_name",
        "description",
        "from_time",
        "to_time",
        "status"
    }

    if not required_cols.issubset(df.columns):
        print("❌ Excel missing required columns:", required_cols)
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
        # LOOP SESSIONS
        # -----------------------------
        for _, row in df.iterrows():

            # CLEAN VALUES
            def clean(val):
                return "" if pd.isna(val) else str(val).strip()

            session_name = clean(row["session_name"])
            description  = clean(row["description"])
            from_time    = clean(row["from_time"])
            to_time      = clean(row["to_time"])
            status       = clean(row["status"])

            if not session_name or not from_time or not to_time:
                print("⏭️ Missing required fields → skipping row")
                continue

            print(f"\n➕ Creating session: {session_name}")

            # -----------------------------
            # OPEN CREATE PAGE
            # -----------------------------
            page.goto(URL, timeout=60000)
            page.wait_for_selector("input[name='session_name']", timeout=60000)

            # -----------------------------
            # FILL FORM
            # -----------------------------
            page.fill("input[name='session_name']", session_name)

            if description:
                page.fill("textarea[name='description']", description)

            page.fill("input[name='from_time']", from_time)
            page.fill("input[name='to_time']", to_time)

            # -----------------------------
            # STATUS (DEFAULT ACTIVE)
            # -----------------------------
            if status in ("0", "1"):
                page.select_option("select[name='status']", status)
            else:
                page.select_option("select[name='status']", "1")

            # -----------------------------
            # SAVE
            # -----------------------------
            page.click("button[type='submit']")
            print(f"✅ Session created: {session_name}")
            time.sleep(2)

        print("\n🎉 All sessions processed")
        input("Press Enter to close browser...")
        browser.close()

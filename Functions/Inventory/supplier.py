from playwright.sync_api import sync_playwright
import pandas as pd
import time
from main import login
import config


def create_suppliers(file_path):
    URL = f"https://{config.restaurant}.foodiee.com.my/inventory/suppliers/create"

    # -----------------------------
    # READ EXCEL / CSV
    # -----------------------------
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    required_cols = {
        "supplier_name",
        "contact_person",
        "phone",
        "email",
        "gst_number",
        "address",
        "payment_terms",
        "credit_limit",
        "rating",
        "bank_details",
    }

    if not required_cols.issubset(df.columns):
        print("❌ Missing required columns:", required_cols)
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
        # LOOP SUPPLIERS
        # -----------------------------
        for _, row in df.iterrows():

            supplier_name = str(row["supplier_name"]).strip()
            if not supplier_name or supplier_name.lower() == "nan":
                print("⏭️ Skipped empty supplier")
                continue

            page.goto(URL, timeout=60000)
            page.wait_for_selector("input[name='supplier_name']", timeout=60000)

            # -----------------------------
            # BASIC INFO
            # -----------------------------
            page.fill("input[name='supplier_name']", supplier_name)
            page.fill("input[name='contact_person']", str(row["contact_person"]))
            page.fill("input[name='phone']", str(row["phone"]))
            page.fill("input[name='email']", str(row["email"]))
            page.fill("input[name='gst_number']", str(row["gst_number"]))

            # -----------------------------
            # ADDRESS
            # -----------------------------
            page.fill("textarea[name='address']", str(row["address"]))

            # -----------------------------
            # PAYMENT TERMS (Select2)
            # -----------------------------
            payment = str(row["payment_terms"]).strip()
            if payment and payment.lower() != "nan":
                page.click("select[name='payment_terms'] + span.select2")
                search = page.locator(".select2-search__field")
                search.fill(payment)
                page.locator(
                    ".select2-results__option",
                    has_text=payment
                ).first.click()

            # -----------------------------
            # CREDIT LIMIT
            # -----------------------------
            credit = row["credit_limit"]
            if pd.isna(credit):
                credit = 0
            page.fill("input[name='credit_limit']", str(credit))

            # -----------------------------
            # RATING (Select2) – search then select
            # -----------------------------
            rating = str(row.get("rating", "")).strip()  # use .get() to avoid KeyError
            
            # Only proceed if there is a valid value
            if rating and rating.lower() != "nan":
                try:
                    # Click to open the dropdown
                    page.click("select[name='rating'] + span.select2")
                
                    # Type into the search field
                    search_box = page.locator(".select2-container--open input.select2-search__field")
                    search_box.fill(rating)  # type the rating, e.g., "3 Stars"
                
                    # Wait for options to populate
                    page.wait_for_selector(".select2-results__option", timeout=5000)
                
                    # Click the matching option
                    page.locator(
                        ".select2-results__option",
                        has_text=f"{rating} Star"
                    ).first.click()
                except Exception as e:
                    print(f"⚠️ Could not set rating '{rating}': {e}")
            else:
                print("⏭ Rating empty, skipping")



            # -----------------------------
            # BANK DETAILS
            # -----------------------------
            page.fill("textarea[name='bank_details']", str(row["bank_details"]))

            # -----------------------------
            # SAVE
            # -----------------------------
            page.click("button[type='submit']")
            print(f"✅ Supplier created: {supplier_name}")

            time.sleep(2)

        browser.close()

# main.py
from playwright.sync_api import sync_playwright
import pandas as pd
from tkinter import filedialog
import config

# restaurant = "ranaacurryhouse"

def login(page, email, password):
    print("🔐 Opening login page...")
    page.goto(f"https://{config.restaurant}.foodiee.com.my/login", timeout=60000)

    page.fill("#email", email)
    page.fill("#password", password)

    print("🧠 Solve captcha and click LOGIN manually...")

    # Wait until redirected after login
    page.wait_for_url("**/dashboard/**", timeout=0)

    print("✅ Login detected")

selected_file_path = None

# ---------------- COMMON FUNCTIONS ----------------
def upload_file(file_label, status_label):
    global selected_file_path

    file_path = filedialog.askopenfilename(
        title="Select Excel / CSV File",
        filetypes=[
            ("Excel Files", "*.xlsx *.xls"),
            ("CSV Files", "*.csv")
        ]
    )

    if file_path:
        selected_file_path = file_path
        file_label.config(text=f"📄 {file_path}")
        status_label.config(text="")

def get_current_item_data(page):
    """Read current item values from edit page"""
    data = {}

    data["food"] = page.input_value("input[name='foodname']").strip()
    data["price"] = page.input_value("input[name='foodprice']").strip()

    data["category"] = page.locator(
        "select[name='CategoryID'] option:checked"
    ).inner_text().strip()

    data["kitchen"] = page.locator(
        "select[name='kitchen'] option:checked"
    ).inner_text().strip()

    data["status"] = page.locator(
        "select[name='status'] option:checked"
    ).get_attribute("value")

    data["extra_notes_limit"] = page.input_value(
        "input[name='extra_notes_limit']"
    ).strip()

    return data
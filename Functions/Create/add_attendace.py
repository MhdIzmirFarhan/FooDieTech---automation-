import pandas as pd
from tkinter import filedialog, messagebox
from datetime import datetime
from playwright.sync_api import sync_playwright
from main import login   # your existing login helper
import time
import config

def upload_attendance_func(window):
    """
    Opens file dialog → reads CSV (skipping first 4 rows) →
    formats attendance data → returns (file_path, formatted_dataframe)
    """

    file_path = filedialog.askopenfilename(
        title="Select Attendance CSV File",
        filetypes=[("CSV Files", "*.csv")]
    )

    if not file_path:
        return None, None

    try:
        # -----------------------------
        # READ CSV SKIPPING FIRST 4 ROWS
        # -----------------------------
        df = pd.read_csv(file_path, skiprows=4)

        # -----------------------------
        # CLEAN COLUMN NAMES
        # -----------------------------
        df.columns = df.columns.str.strip().str.lower()

        required_columns = ["name", "date", "punch 1", "punch 2"]

        for col in required_columns:
            if col not in df.columns:
                messagebox.showerror(
                    "Error",
                    f"Missing required column: {col}"
                )
                return None, None

        formatted_rows = []

        for _, row in df.iterrows():
            name = str(row["name"]).strip() if not pd.isna(row["name"]) else ""
            date = str(row["date"]).strip() if not pd.isna(row["date"]) else ""

            punch1 = str(row["punch 1"]).strip() if not pd.isna(row["punch 1"]) else ""
            punch2 = str(row["punch 2"]).strip() if not pd.isna(row["punch 2"]) else ""

            stay_time = ""

            # -----------------------------
            # CALCULATE STAY TIME
            # -----------------------------
            try:
                if punch1 and punch2:
                    time_format = "%H:%M:%S" if len(punch1.split(":")) == 3 else "%H:%M"

                    t1 = datetime.strptime(punch1, time_format)
                    t2 = datetime.strptime(punch2, time_format)

                    duration = t2 - t1

                    total_seconds = int(duration.total_seconds())
                    hours = total_seconds // 3600
                    minutes = (total_seconds % 3600) // 60

                    stay_time = f"{hours}h {minutes}m"

            except Exception:
                stay_time = "Invalid Time"

            formatted_rows.append({
                "name": name,
                "date": date,
                "check_in": punch1,
                "check_out": punch2,
                "stay_time": stay_time
            })

        formatted_df = pd.DataFrame(formatted_rows)

        messagebox.showinfo("Success", "Attendance file loaded successfully!")

        return file_path, formatted_df

    except Exception as e:
        messagebox.showerror("Error", f"Failed to read file:\n{e}")
        return None, None

def upload_attendance_to_hrm(window):
    if not hasattr(window, "attendance_df") or window.attendance_df is None:
        messagebox.showerror("Error", "Upload attendance file first!")
        return
    
    df = window.attendance_df

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=80)
        context = browser.new_context()
        page = context.new_page()
    
        # LOGIN FIRST
        login(page, "admin@gmail.com", "FooDiee#25!")

        page.goto(
            f"https://{config.restaurant}.foodiee.com.my/hrm/Home/index",
            wait_until="networkidle"
        )

        for _, row in df.iterrows():
            employee_name = str(row["name"]).strip()
        
            if not employee_name:
                continue

            page.click("button[data-target='#add0']")
            page.wait_for_selector("#select2-employee_id-container", timeout=5000)

            page.click("#select2-employee_id-container")

            search_input = page.locator(".select2-container--open .select2-search__field")
            search_input.wait_for(state="visible", timeout=5000)
            search_input.fill(employee_name)
            search_input.press("Enter")

            page.click("button.btn.btn-success.w-md.m-b-5")
            time.sleep(1)

        browser.close()
        messagebox.showinfo("Success", "Attendance uploaded successfully!")
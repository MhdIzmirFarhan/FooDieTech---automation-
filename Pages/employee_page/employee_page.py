import tkinter as tk
from tkinter import ttk, messagebox
from Functions.Create import add_employee
from playwright.sync_api import sync_playwright
from main import login   # your reusable login function
import config
import time
import pandas as pd


def open_employee_page():
    window = tk.Toplevel()
    window.title("Employee Management")
    window.state("zoomed")
    window.configure(bg="#f9fafb")

    # =============================
    # TABLE DISPLAY FRAME
    # =============================
    table_frame = tk.Frame(window, bg="white")
    table_frame.pack(fill="both", expand=True, padx=20, pady=10)

    style = ttk.Style()
    style.configure("Treeview", rowheight=28, font=("Segoe UI", 10))
    style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

    tree = ttk.Treeview(table_frame)
    tree.pack(fill="both", expand=True)

    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # =============================
    # LOAD EMPLOYEE DATA
    # =============================
    def load_table_data():
        tree.delete(*tree.get_children())

        columns = (
            "Name",
            "Email",
            "Contact Number",
            "Employee Type",
            "Designation"
        )

        tree["columns"] = columns
        tree["show"] = "headings"

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=180)

        if hasattr(window, "employee_df"):
            for _, row in window.employee_df.iterrows():
                tree.insert("", "end", values=(
                    row["name"],
                    row["contact_email"],
                    row["contact_number"],
                    row["employee_type"],
                    row["designation"]
                ))

    load_table_data()

    # =============================
    # BUTTON FRAME
    # =============================
    btn_frame = tk.Frame(window, bg="#f9fafb")
    btn_frame.pack(fill="x", pady=15)

    button_style = {
        "width": 25,
        "height": 2,
        "bd": 0,
        "bg": "#111827",
        "fg": "white",
        "activebackground": "#374151",
        "activeforeground": "white"
    }

    # -----------------------------
    # UPLOAD EMPLOYEE FILE
    # -----------------------------
    def handle_upload_employee():
        file_path, df = add_employee.upload_employee_func(window)

        if df is not None:
            window.employee_df = df
            window.employee_file = file_path
            load_table_data()

    # -----------------------------
    # UPLOAD EMPLOYEES TO HRM
    # -----------------------------
    def handle_upload_employee_to_hrm():
        df = getattr(window, "employee_df", None)
    
        if df is None:
            messagebox.showerror("Error", "Please upload employee file first.")
            return
    
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=False, slow_mo=80)
                context = browser.new_context()
                page = context.new_page()
    
                # -----------------------------
                # LOGIN FIRST
                # -----------------------------
                login(
                    page,
                    email="admin@gmail.com",      # change if needed
                    password="FooDiee#25!"        # change if needed
                )
    
                messagebox.showinfo(
                    "CAPTCHA Required",
                    "Please solve CAPTCHA and click Login.\n"
                    "Press OK once you are logged in."
                )
    
                page.wait_for_load_state("networkidle")
    
                # -----------------------------
                # GO TO HRM EMPLOYEE PAGE
                # -----------------------------
                page.goto(
                    f"https://{config.restaurant}.foodiee.com.my/hrm/Employees/viewEmhistory",
                    timeout=60000
                )
                page.wait_for_selector("input#first_name", timeout=60000)
    
                # -----------------------------
                # LOOP THROUGH EMPLOYEES
                # -----------------------------
                for _, row in df.iterrows():
                    first_name = "" if pd.isna(row["name"]) else str(row["name"]).strip()
                    email = "" if pd.isna(row["contact_email"]) else str(row["contact_email"]).strip()
                    phone = "" if pd.isna(row["contact_number"]) else str(row["contact_number"]).strip()
                    designation = "" if pd.isna(row.get("designation", "")) else str(row.get("designation")).strip()
                    start_date = "" if pd.isna(row.get("start_date", "")) else str(row.get("start_date")).strip()
    
                    if not first_name:
                        continue
    
                    print(f"➕ Creating employee: {first_name}")
    
                    # -----------------------------
                    # FILL MAIN FIELDS
                    # -----------------------------
                    page.fill("input#first_name", first_name)
                    page.fill("input#email", email)
                    page.fill("input#phone", phone)
    
                    # -----------------------------
                    # CLICK NEXT (first page)
                    # -----------------------------
                    page.click("input.btnNext")
                    page.wait_for_timeout(1000)
    
                    # -----------------------------
                    # FILL DIVISION (default "Waiter")
                    # -----------------------------
                    page.click("span#select2-division-container")
                    page.fill("input.select2-search__field", "Waiter")  # default
                    page.keyboard.press("Enter")
                    page.wait_for_timeout(300)
    
                    # -----------------------------
                    # FILL DESIGNATION (from CSV)
                    # -----------------------------
                    if designation:
                        page.click("span#select2-designation-container")
                        page.fill("input.select2-search__field", designation)
                        page.keyboard.press("Enter")
                        page.wait_for_timeout(300)
    
                    # -----------------------------
                    # FILL DATE FIELDS WITH DEFAULT 2001-01-01 BY TYPING AND FIRE EVENTS
                    # -----------------------------
                    for selector in ["input#ohiredate", "input#hiredate"]:
                        page.fill(selector, "2001-01-01")
                        page.dispatch_event(selector, "input")
                        page.dispatch_event(selector, "change")
                        page.dispatch_event(selector, "blur")  # important
                        page.wait_for_timeout(200)  # small delay to let JS process
    
                    # -----------------------------
                    # FILL RATE TYPE (default "Salary")
                    # -----------------------------
                    page.click("span#select2-rate_type-container")
                    page.fill("input.select2-search__field", "Salary")
                    page.keyboard.press("Enter")
                    page.wait_for_timeout(200)
    
                    # -----------------------------
                    # FILL PAY FREQUENCY (default "Monthly")
                    # -----------------------------
                    page.click("span#select2-pay_frequency-container")
                    page.fill("input.select2-search__field", "Monthly")
                    page.keyboard.press("Enter")
                    page.wait_for_timeout(200)
    
                    # -----------------------------
                    # FILL RATE (default 0)
                    # -----------------------------
                    page.fill("input#rate", "0")
    
                    # -----------------------------
                    # CLICK NEXT (second page)
                    # -----------------------------
                    # Specifically pick the Next button with onclick valid_inf2()
                    page.wait_for_selector('input.btnNext[onclick="valid_inf2()"]', timeout=5000)
                    page.click('input.btnNext[onclick="valid_inf2()"]')
                    page.wait_for_timeout(1000)


                    page.wait_for_selector('input.btnNext[onclick="valid_inf4()"]', timeout=5000)
                    page.click('input.btnNext[onclick="valid_inf4()"]')
                    page.wait_for_timeout(1000)
    
                    # -----------------------------
                    # DOB AND GENDER SECTION
                    # -----------------------------
                    page.fill("input#dob", "2001-04-22")  # Default DOB
                    page.click("span#select2-gender-container")
                    page.fill("input.select2-search__field", "Others")  # Default gender
                    page.keyboard.press("Enter")
                    page.wait_for_timeout(300)
    
                    # CLICK NEXT (third page)
                     # Specifically pick the Next button with onclick valid_inf5()
                    page.wait_for_selector('input.btnNext[onclick="valid_inf5()"]', timeout=5000)
                    page.click('input.btnNext[onclick="valid_inf5()"]')
                    page.wait_for_timeout(1000)
    
                    # -----------------------------
                    # EMERGENCY CONTACTS
                    # -----------------------------
                    page.fill("input#em_contact", "0")
                    page.fill("input#e_w_phone", "0")
                    page.fill("input#e_h_phone", "0")
    
                    # -----------------------------
                    # SAVE EMPLOYEE
                    # -----------------------------
                    # Wait for the Save button to appear and click it
                    page.wait_for_selector('input.btn-success[onclick="valid_inf8()"]', timeout=5000)
                    page.click('input.btn-success[onclick="valid_inf8()"]')
                    page.wait_for_timeout(1000)
    
                    # -----------------------------
                    # RETURN TO EMPLOYEE FORM FOR NEXT ROW
                    # -----------------------------
                    page.goto(
                        f"https://{config.restaurant}.foodiee.com.my/hrm/Employees/viewEmhistory",
                        timeout=60000
                    )
                    page.wait_for_selector("input#first_name", timeout=60000)
    
                messagebox.showinfo("Success", "All employees uploaded to HRM!")
    
                browser.close()
    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload employees:\n{e}")

    # =============================
    # BUTTONS
    # =============================
    tk.Button(
        btn_frame,
        text="Upload Employees",
        command=handle_upload_employee,
        **button_style
    ).pack(side="left", padx=10)

    tk.Button(
        btn_frame,
        text="Upload Employees To HRM",
        command=handle_upload_employee_to_hrm,
        **button_style
    ).pack(side="left", padx=10)
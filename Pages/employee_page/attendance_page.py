import tkinter as tk
from tkinter import ttk, messagebox
from Functions.Create.add_attendace import (
    upload_attendance_func,
    upload_attendance_to_hrm
)
import threading  # <-- import threading for background tasks

def open_attendance_page():
    window = tk.Toplevel()
    window.title("Attendance Management")
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
    # LOAD ATTENDANCE DATA
    # =============================
    def load_table_data():
        tree.delete(*tree.get_children())

        # -----------------------------
        # DEFINE COLUMNS FIRST
        # -----------------------------
        columns = (
            "Employee Name",
            "Date",
            "Check In",
            "Check Out",
            "Stay Time"
        )

        tree["columns"] = columns
        tree["show"] = "headings"

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=180)

        # -----------------------------
        # POPULATE ROWS
        # -----------------------------
        if hasattr(window, "attendance_df"):
            for _, row in window.attendance_df.iterrows():
                tree.insert("", "end", values=(
                    row.get("name", ""),
                    row.get("date", ""),
                    row.get("check_in", ""),
                    row.get("check_out", ""),
                    row.get("stay_time", "")
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
    # UPLOAD ATTENDANCE FILE
    # -----------------------------
    def handle_upload_attendance():
        file_path, df = upload_attendance_func(window)

        if df is not None:
            window.attendance_df = df
            window.attendance_file = file_path
            load_table_data()

    # -----------------------------
    # UPLOAD ATTENDANCE TO HRM
    # -----------------------------
    # def handle_upload_attendance_to_hrm():
    #     if not hasattr(window, "attendance_df") or window.attendance_df.empty:
    #         messagebox.showerror("Error", "Please upload attendance CSV first!")
    #         return
    #     if not hasattr(window, "attendance_file"):
    #         messagebox.showerror("Error", "Attendance file path missing!")
    #         return
        
    #     # -----------------------------
    #     # RUN PLAYWRIGHT IN BACKGROUND THREAD
    #     # -----------------------------
    #     def run_upload():
    #         from Functions.Create.add_attendace import upload_to_hrm
    #         upload_to_hrm(window.attendance_file, window.attendance_df)
        
    #     threading.Thread(target=run_upload, daemon=True).start()

    def handle_upload_attendance_to_hrm():
        upload_attendance_to_hrm(window)

    # =============================
    # BUTTONS
    # =============================
    tk.Button(
        btn_frame,
        text="Upload Attendance",
        command=handle_upload_attendance,
        **button_style
    ).pack(side="left", padx=10)

    tk.Button(
        btn_frame,
        text="Upload Attendance To HRM",
        command=handle_upload_attendance_to_hrm,
        **button_style
    ).pack(side="left", padx=10)
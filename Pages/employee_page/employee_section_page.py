import tkinter as tk
from .employee_page import open_employee_page
from ..employee_page.attendance_page import open_attendance_page

def open_employee_section_page():
    window = tk.Toplevel()
    window.title("Employee Section")
    window.geometry("400x300")
    window.configure(bg="#f9fafb")

    button_style = {
        "width": 25,
        "height": 2,
        "bd": 0,
        "bg": "#111827",
        "fg": "white",
        "activebackground": "#374151",
        "activeforeground": "white"
    }

    tk.Button(
        window,
        text="Employee Management",
        command=open_employee_page,
        **button_style
    ).pack(pady=20)

    tk.Button(
        window,
        text="Attendance Management",
        command=open_attendance_page,
        **button_style
    ).pack(pady=10)
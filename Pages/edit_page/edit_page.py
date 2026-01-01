# import tkinter as tk
# from tkinter import filedialog
# import tkinter.messagebox as messagebox
# import threading
# from Functions.Edit.edit_details import edit_items_from_excel    

# def open_edit_item_page(upload_file, selected_file_path):
#     print("File:", selected_file_path)
#     upload_file(selected_file_path)

#     edit_win = tk.Toplevel()
#     edit_win.title("Edit Food Items")
#     edit_win.geometry("520x360")
#     edit_win.resizable(False, False)

#     tk.Label(edit_win, text="Upload Excel / CSV File", font=("Segoe UI", 12)).pack(pady=10)

#     file_label = tk.Label(edit_win, text="No file selected", fg="gray", wraplength=480)
#     file_label.pack()

#     status_label = tk.Label(edit_win, text="", fg="blue")
#     status_label.pack(pady=5)

#     tk.Button(
#         edit_win,
#         text="📂 Upload File",
#         width=20,
#         command=lambda: upload_file(file_label, status_label)
#     ).pack(pady=5)

#     # MAX ID INPUT
#     tk.Label(edit_win, text="Max Item ID (e.g. 303)").pack(pady=(15, 5))
#     max_id_entry = tk.Entry(edit_win, width=10)
#     max_id_entry.pack()

#     def start_edit_bot():
#         if not selected_file_path:
#             status_label.config(text="❌ Please upload a file")
#             return

#         if not max_id_entry.get().isdigit():
#             status_label.config(text="❌ Enter valid max ID")
#             return

#         status_label.config(text="✏️ Editing items...")
#         threading.Thread(
#             target=edit_items_from_excel,
#             args=(selected_file_path, int(max_id_entry.get())),
#             daemon=True
#         ).start()

#     tk.Button(
#         edit_win,
#         text="▶ Run Edit Automation",
#         width=25,
#         bg="#f39c12",
#         fg="white",
#         command=start_edit_bot
#     ).pack(pady=25)


# Pages/edit_page/edit_page.py

import tkinter as tk
from tkinter import filedialog
import threading
from Functions.Edit.edit_details import edit_items_from_excel

# ---------------- GLOBAL ----------------
selected_file_path = None


def upload_file(file_label, status_label):
    global selected_file_path
    file_path = filedialog.askopenfilename(
        filetypes=[("Excel Files", "*.xlsx *.csv")]
    )

    if not file_path:
        return

    selected_file_path = file_path
    file_label.config(text=file_path, fg="black")
    status_label.config(text="✅ File loaded", fg="green")


def open_edit_item_page(status_label):
    edit_win = tk.Toplevel()
    edit_win.title("Edit Food Items")
    edit_win.geometry("520x360")
    edit_win.resizable(False, False)

    tk.Label(edit_win, text="Upload Excel / CSV File", font=("Segoe UI", 12)).pack(pady=10)

    file_label = tk.Label(edit_win, text="No file selected", fg="gray", wraplength=480)
    file_label.pack()

    page_status = tk.Label(edit_win, text="", fg="blue")
    page_status.pack(pady=5)

    tk.Button(
        edit_win,
        text="📂 Upload File",
        width=20,
        command=lambda: upload_file(file_label, page_status)
    ).pack(pady=5)

    # MAX ID INPUT
    tk.Label(edit_win, text="Max Item ID (e.g. 303)").pack(pady=(15, 5))
    max_id_entry = tk.Entry(edit_win, width=10)
    max_id_entry.pack()

    def start_edit_bot():
        if not selected_file_path:
            page_status.config(text="❌ Please upload a file", fg="red")
            return

        if not max_id_entry.get().isdigit():
            page_status.config(text="❌ Enter valid max ID", fg="red")
            return

        page_status.config(text="✏️ Editing items...", fg="blue")
        status_label.config(text="Editing food items...", fg="blue")

        threading.Thread(
            target=edit_items_from_excel,
            args=(selected_file_path, int(max_id_entry.get())),
            daemon=True
        ).start()

    tk.Button(
        edit_win,
        text="▶ Run Edit Automation",
        width=25,
        bg="#f39c12",
        fg="white",
        command=start_edit_bot
    ).pack(pady=25)

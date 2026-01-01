import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as messagebox
import threading    
from Functions.Analyze.analyze import analyze_items_by_id

def open_analysis_page(upload_file, selected_file_path):
    print("File:", selected_file_path)
    upload_file(selected_file_path)

    analysis_win = tk.Toplevel()
    analysis_win.title("Analyze Food Items")
    analysis_win.geometry("520x300")
    analysis_win.resizable(False, False)

    tk.Label(
        analysis_win,
        text="Analyze Excel vs System",
        font=("Segoe UI", 13, "bold")
    ).pack(pady=15)

    file_label = tk.Label(
        analysis_win,
        text="No file selected",
        fg="gray",
        wraplength=480
    )
    file_label.pack(pady=5)

    status_label = tk.Label(analysis_win, text="", fg="blue")
    status_label.pack(pady=5)

    tk.Button(
        analysis_win,
        text="📂 Upload Excel / CSV",
        width=25,
        command=lambda: upload_file(file_label, status_label)
    ).pack(pady=5)

    def start_analysis():
        if not selected_file_path:
            status_label.config(text="❌ Please upload an Excel file")
            return

        status_label.config(text="🔍 Analyzing data...")
        threading.Thread(
            target=analyze_items_by_id,
            args=(selected_file_path, 350),
            daemon=True
        ).start()

    tk.Button(
        analysis_win,
        text="▶ Run Analysis",
        width=25,
        bg="#9b59b6",
        fg="white",
        command=start_analysis
    ).pack(pady=25)
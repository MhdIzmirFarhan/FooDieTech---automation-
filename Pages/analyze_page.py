# analyze_page.py
import tkinter as tk
from tkinter import filedialog
import threading
import sys
from Functions.Analyze.analyze import analyze_items_from_excel


# ================== STDOUT REDIRECT ==================
class TextRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.after(0, lambda: self._append(text))

    def _append(self, text):
        self.widget.insert("end", text)
        self.widget.see("end")

    def flush(self):
        pass


def open_analysis_page(selected_file_path_var, main_status_label):

    # ---------------- WINDOW ----------------
    analysis_win = tk.Toplevel()
    analysis_win.title("Analyze Food Items")
    analysis_win.state("zoomed")  # Fullscreen

    # ================== HEADER ==================
    header_frame = tk.Frame(analysis_win)
    header_frame.pack(fill="x", pady=(15, 5))

    tk.Label(
        header_frame,
        text="Analyze Excel vs System",
        font=("Segoe UI", 16, "bold")
    ).pack()

    tk.Label(
        header_frame,
        text="Compare Excel items against system records",
        font=("Segoe UI", 10),
        fg="gray"
    ).pack(pady=(2, 10))

    # ================== TOP CONTROLS ==================
    top_frame = tk.Frame(analysis_win)
    top_frame.pack(fill="x", padx=20)

    # FILE DISPLAY
    file_label = tk.Label(
        top_frame,
        text=selected_file_path_var.get() or "No file selected",
        fg="gray",
        anchor="w"
    )
    file_label.pack(side="left", expand=True, fill="x")

    def choose_file():
        path = filedialog.askopenfilename(
            title="Select Excel / CSV File",
            filetypes=[("Excel Files", "*.xlsx *.csv")]
        )
        if path:
            filename = path.split("/")[-1]
            selected_file_path_var.set(path)
            file_label.config(text=filename, fg="green")
            main_status_label.config(text=f"Selected file: {filename}", fg="#2980b9")

    tk.Button(
        top_frame,
        text="📂 Upload Excel / CSV",
        bg="#3498db",
        fg="white",
        width=22,
        command=choose_file
    ).pack(side="right", padx=10)

    # ================== OUTPUT AREA ==================
    output_frame = tk.LabelFrame(
        analysis_win,
        text=" Analysis Output ",
        font=("Segoe UI", 9, "bold"),
        padx=10,
        pady=10
    )
    output_frame.pack(fill="both", expand=True, padx=20, pady=15)

    text_area = tk.Text(
        output_frame,
        wrap="word",
        font=("Consolas", 10),
        bg="#0f172a",
        fg="#e5e7eb",
        insertbackground="white"
    )
    text_area.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(output_frame, command=text_area.yview)
    scrollbar.pack(side="right", fill="y")
    text_area.config(yscrollcommand=scrollbar.set)

    # ================== STATUS BAR ==================
    status_label = tk.Label(
        analysis_win,
        text="",
        fg="#2980b9",
        font=("Segoe UI", 10, "bold")
    )
    status_label.pack(pady=(0, 10))

    # ================== RUN ANALYSIS ==================
    def start_analysis():
        file_path = selected_file_path_var.get()
        if not file_path:
            status_label.config(text="❌ Please upload an Excel file", fg="red")
            return

        text_area.delete("1.0", "end")
        status_label.config(text="🔍 Analyzing data...", fg="#2980b9")
        main_status_label.config(text="Analyzing data...", fg="#2980b9")

        def run():
            old_stdout = sys.stdout
            sys.stdout = TextRedirector(text_area)

            try:
                analyze_items_from_excel(file_path)
                status_label.config(text="✅ Analysis complete", fg="green")
                main_status_label.config(text="Analysis complete", fg="green")
            except Exception as e:
                print(f"\n❌ ERROR: {e}")
                status_label.config(text="❌ Analysis failed", fg="red")
            finally:
                sys.stdout = old_stdout

        threading.Thread(target=run, daemon=True).start()

    tk.Button(
        analysis_win,
        text="▶ Run Analysis",
        bg="#9b59b6",
        fg="white",
        font=("Segoe UI", 11, "bold"),
        width=25,
        command=start_analysis
    ).pack(pady=10)

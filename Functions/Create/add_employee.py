import pandas as pd
from tkinter import filedialog, messagebox


# -----------------------------
# Upload Employee CSV (Detect Header + Clean Columns)
# -----------------------------
def upload_employee_func(root):
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV Files", "*.csv *.CSV")]
    )

    if not file_path:
        return None, None

    try:
        # Read raw file (no header)
        df_raw = pd.read_csv(file_path, encoding="utf-8-sig", header=None)

        header_row_index = None

        # Detect header row dynamically
        for i, row in df_raw.iterrows():
            row_values = [str(cell).strip().lower() for cell in row.tolist()]

            if (
                "name" in row_values and
                "contact email" in row_values and
                "contact number" in row_values
            ):
                header_row_index = i
                break

        if header_row_index is None:
            messagebox.showerror("Error", "Could not detect header row.")
            return None, None

        # Re-read file using detected header
        df = pd.read_csv(
            file_path,
            encoding="utf-8-sig",
            header=header_row_index
        )

        # Clean column names safely
        df.columns = (
            df.columns.astype(str)
            .str.strip()
            .str.lower()
            .str.replace(" ", "_", regex=False)
        )

        # Remove completely empty rows
        df = df.dropna(how="all")

        required_cols = [
            "name",
            "contact_email",
            "contact_number",
            "employee_type",
            "designation"
        ]

        missing = [col for col in required_cols if col not in df.columns]

        if missing:
            messagebox.showerror(
                "Error",
                f"Missing columns: {missing}\n\nDetected columns:\n{df.columns.tolist()}"
            )
            return None, None

        # Keep only required columns (clean dataframe)
        df = df[required_cols]

        return file_path, df.reset_index(drop=True)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to load file:\n{e}")
        return None, None
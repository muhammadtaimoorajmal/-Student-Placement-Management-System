import csv
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

def export_to_csv(data, headers, filename_prefix="report"):
    """Export list of dictionaries to CSV file."""
    if not data:
        messagebox.showwarning("No Data", "Nothing to export.")
        return
    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        initialfile=f"{filename_prefix}.csv"
    )
    if file_path:
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
        messagebox.showinfo("Success", f"Exported to {file_path}")

def export_to_excel(data, headers, filename_prefix="report"):
    """Export to Excel using pandas."""
    if not data:
        messagebox.showwarning("No Data", "Nothing to export.")
        return
    file_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel files", "*.xlsx")],
        initialfile=f"{filename_prefix}.xlsx"
    )
    if file_path:
        df = pd.DataFrame(data)
        df.to_excel(file_path, index=False)
        messagebox.showinfo("Success", f"Exported to {file_path}")

def export_to_pdf(data, headers, filename_prefix="report"):
    """Export to PDF using reportlab."""
    if not data:
        messagebox.showwarning("No Data", "Nothing to export.")
        return
    file_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")],
        initialfile=f"{filename_prefix}.pdf"
    )
    if file_path:
        doc = SimpleDocTemplate(file_path, pagesize=letter)
        elements = []
        table_data = [headers] + [list(row.values()) for row in data]
        t = Table(table_data)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
        ]))
        elements.append(t)
        doc.build(elements)
        messagebox.showinfo("Success", f"Exported to {file_path}")

def center_window(window, width, height):
    """Center a Tkinter window on screen."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")
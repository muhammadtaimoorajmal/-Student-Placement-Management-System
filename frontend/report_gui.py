import tkinter as tk
from tkinter import ttk, messagebox
from backend import report_ops
from utils.helpers import export_to_csv

class ReportWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Placement Reports")
        self.window.geometry("900x700")
        self.window.configure(bg='#f0f0f0')

        notebook = ttk.Notebook(self.window)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Report 1: Companies with Jobs
        self.frame1 = tk.Frame(notebook, bg='#ffffff')
        notebook.add(self.frame1, text="Companies & Job Counts")
        self.load_report(self.frame1, report_ops.get_report_companies_with_jobs, "companies_jobs")

        # Report 2: Applications by Status
        self.frame2 = tk.Frame(notebook, bg='#ffffff')
        notebook.add(self.frame2, text="Applications by Status")
        self.load_report(self.frame2, report_ops.get_report_applications_by_status, "app_status")

        # Report 3: Department Placement Stats
        self.frame3 = tk.Frame(notebook, bg='#ffffff')
        notebook.add(self.frame3, text="Department Placement Stats")
        self.load_report(self.frame3, report_ops.get_report_department_placement_stats, "dept_stats")

    def load_report(self, parent, data_func, filename_prefix):
        data = data_func()
        if not data:
            tk.Label(parent, text="No data available.", font=("Arial", 14), bg='#ffffff').pack(pady=50)
            return
        # Treeview
        columns = list(data[0].keys())
        tree = ttk.Treeview(parent, columns=columns, show='headings', height=20)
        for col in columns:
            tree.heading(col, text=col.replace('_', ' ').title())
            tree.column(col, width=150)
        tree.pack(fill='both', expand=True, padx=10, pady=10)
        for row in data:
            tree.insert('', tk.END, values=list(row.values()))
        # Export button
        btn = tk.Button(parent, text="Export to CSV", command=lambda: export_to_csv(data, columns, filename_prefix), bg='#4CAF50', fg='white', padx=10)
        btn.pack(pady=5)
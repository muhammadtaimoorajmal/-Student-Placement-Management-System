import tkinter as tk
from tkinter import ttk, messagebox
from backend import tpo_ops, report_ops
from frontend.report_gui import ReportWindow

class TPODashboard:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("TPO Admin Dashboard")
        self.window.geometry("900x650")
        self.window.configure(bg='#e8f4f8')

        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Tabs
        self.students_tab = tk.Frame(self.notebook, bg='#ffffff')
        self.notebook.add(self.students_tab, text="Students")
        self.load_students()

        self.companies_tab = tk.Frame(self.notebook, bg='#ffffff')
        self.notebook.add(self.companies_tab, text="Companies")
        self.load_companies()

        self.jobs_tab = tk.Frame(self.notebook, bg='#ffffff')
        self.notebook.add(self.jobs_tab, text="Jobs")
        self.load_jobs()

        self.apps_tab = tk.Frame(self.notebook, bg='#ffffff')
        self.notebook.add(self.apps_tab, text="Applications")
        self.load_applications()

        self.reports_tab = tk.Frame(self.notebook, bg='#ffffff')
        self.notebook.add(self.reports_tab, text="Reports")
        self.setup_reports()

        self.window.mainloop()

    def load_students(self):
        for widget in self.students_tab.winfo_children():
            widget.destroy()
        students = tpo_ops.get_all_students()
        if not students:
            tk.Label(self.students_tab, text="No students found.", font=("Arial", 14), bg='#ffffff').pack(pady=50)
            return
        tree = ttk.Treeview(self.students_tab)
        tree.pack(fill='both', expand=True, padx=10, pady=10)
        if students:
            columns = list(students[0].keys())
            tree['columns'] = columns
            tree['show'] = 'headings'
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=100)
            for row in students:
                tree.insert('', tk.END, values=list(row.values()))

    def load_companies(self):
        for widget in self.companies_tab.winfo_children():
            widget.destroy()
        companies = tpo_ops.get_all_companies()
        if not companies:
            tk.Label(self.companies_tab, text="No companies found.", font=("Arial", 14), bg='#ffffff').pack(pady=50)
            return
        tree = ttk.Treeview(self.companies_tab)
        tree.pack(fill='both', expand=True, padx=10, pady=10)
        if companies:
            columns = list(companies[0].keys())
            tree['columns'] = columns
            tree['show'] = 'headings'
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=120)
            for row in companies:
                tree.insert('', tk.END, values=list(row.values()))
        # Verify button
        def verify():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Select a company to verify.")
                return
            company_id = tree.item(selected[0])['values'][0]
            if tpo_ops.verify_company(company_id):
                messagebox.showinfo("Success", f"Company {company_id} verified.")
                self.load_companies()  # refresh
            else:
                messagebox.showerror("Error", "Verification failed.")
        btn = tk.Button(self.companies_tab, text="Verify Selected Company", command=verify, bg='#4CAF50', fg='white')
        btn.pack(pady=10)

    def load_jobs(self):
        for widget in self.jobs_tab.winfo_children():
            widget.destroy()
        jobs = tpo_ops.get_all_jobs()
        if not jobs:
            tk.Label(self.jobs_tab, text="No jobs found.", font=("Arial", 14), bg='#ffffff').pack(pady=50)
            return
        tree = ttk.Treeview(self.jobs_tab)
        tree.pack(fill='both', expand=True, padx=10, pady=10)
        if jobs:
            columns = list(jobs[0].keys())
            tree['columns'] = columns
            tree['show'] = 'headings'
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=120)
            for row in jobs:
                tree.insert('', tk.END, values=list(row.values()))

    def load_applications(self):
        for widget in self.apps_tab.winfo_children():
            widget.destroy()
        apps = tpo_ops.get_all_applications()
        if not apps:
            tk.Label(self.apps_tab, text="No applications found.", font=("Arial", 14), bg='#ffffff').pack(pady=50)
            return
        tree = ttk.Treeview(self.apps_tab)
        tree.pack(fill='both', expand=True, padx=10, pady=10)
        if apps:
            columns = list(apps[0].keys())
            tree['columns'] = columns
            tree['show'] = 'headings'
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=120)
            for row in apps:
                tree.insert('', tk.END, values=list(row.values()))

    def setup_reports(self):
        for widget in self.reports_tab.winfo_children():
            widget.destroy()
        btn = tk.Button(self.reports_tab, text="View Detailed Reports", command=lambda: ReportWindow(self.window), font=("Arial", 14), bg='#2196F3', fg='white', padx=20, pady=10)
        btn.pack(expand=True)
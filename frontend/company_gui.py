import tkinter as tk
from tkinter import ttk, messagebox
from backend import company_ops
from utils.helpers import center_window
from datetime import datetime

class CompanyDashboard:
    def __init__(self, company_id):
        self.company_id = company_id
        self.window = tk.Tk()
        self.window.title(f"Company Dashboard - {company_id}")
        center_window(self.window, 1000, 700)
        self.window.configure(bg='#e8f4f8')

        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Profile tab
        self.profile_tab = tk.Frame(self.notebook, bg='#ffffff')
        self.notebook.add(self.profile_tab, text="🏢 Profile")
        self.load_profile()

        # My Jobs tab
        self.jobs_tab = tk.Frame(self.notebook, bg='#ffffff')
        self.notebook.add(self.jobs_tab, text="📌 My Job Postings")
        self.load_my_jobs()

        # Post Job tab
        self.post_job_tab = tk.Frame(self.notebook, bg='#ffffff')
        self.notebook.add(self.post_job_tab, text="➕ Post New Job")
        self.setup_post_job_form()

        # Applicants tab
        self.applicants_tab = tk.Frame(self.notebook, bg='#ffffff')
        self.notebook.add(self.applicants_tab, text="👥 Applicants")
        self.load_applicants()

        self.window.mainloop()

    def load_profile(self):
        for widget in self.profile_tab.winfo_children():
            widget.destroy()
        data = company_ops.get_company_details(self.company_id)
        if not data:
            messagebox.showerror("Error", "Could not load profile")
            return
        frame = tk.Frame(self.profile_tab, bg='#ffffff', padx=30, pady=30)
        frame.pack(fill='both', expand=True)
        labels = ["Company ID:", "Name:", "Industry:", "Email:", "Phone:", "Address:", "TPO Verified:"]
        keys = ['COMPANY_ID', 'COMPANY_NAME', 'INDUSTRY', 'EMAIL', 'PHONE', 'ADDRESS', 'TPO_VERIFIED']
        for i, (label, key) in enumerate(zip(labels, keys)):
            tk.Label(frame, text=label, font=("Arial", 12, "bold"), bg='#ffffff', anchor='e').grid(row=i, column=0, sticky='e', padx=10, pady=8)
            tk.Label(frame, text=data.get(key, 'N/A'), font=("Arial", 12), bg='#ffffff', anchor='w').grid(row=i, column=1, sticky='w', padx=10, pady=8)

    def load_my_jobs(self):
        for widget in self.jobs_tab.winfo_children():
            widget.destroy()
        jobs = company_ops.get_company_jobs(self.company_id)
        if not jobs:
            tk.Label(self.jobs_tab, text="No jobs posted yet.", font=("Arial", 14), bg='#ffffff').pack(pady=50)
            return
        columns = ('JOB_ID', 'JOB_TITLE', 'REQUIRED_CGPA', 'LOCATION', 'DEADLINE_DATE', 'IS_ACTIVE')
        tree = ttk.Treeview(self.jobs_tab, columns=columns, show='headings', height=15)
        for col in columns:
            tree.heading(col, text=col.replace('_', ' '))
            tree.column(col, width=120)
        tree.pack(fill='both', expand=True, padx=10, pady=10)
        for job in jobs:
            tree.insert('', tk.END, values=(job['JOB_ID'], job['JOB_TITLE'], job['REQUIRED_CGPA'], job['LOCATION'], job['DEADLINE_DATE'], job['IS_ACTIVE']))
        tk.Button(self.jobs_tab, text="Refresh", command=self.load_my_jobs, bg='#2196F3', fg='white').pack(pady=5)

    def setup_post_job_form(self):
        for widget in self.post_job_tab.winfo_children():
            widget.destroy()
        frame = tk.Frame(self.post_job_tab, bg='#ffffff', padx=30, pady=30)
        frame.pack(fill='both', expand=True)

        fields = ['Job Title', 'Description', 'Required CGPA', 'Location', 'Deadline (YYYY-MM-DD)']
        entries = {}
        for i, field in enumerate(fields):
            tk.Label(frame, text=field+":", font=("Arial", 12), bg='#ffffff').grid(row=i, column=0, sticky='e', padx=10, pady=10)
            entry = tk.Entry(frame, width=40)
            entry.grid(row=i, column=1, padx=10, pady=10)
            entries[field] = entry

        def post():
            title = entries['Job Title'].get()
            desc = entries['Description'].get()
            try:
                cgpa = float(entries['Required CGPA'].get())
            except:
                messagebox.showerror("Error", "CGPA must be a number")
                return
            loc = entries['Location'].get()
            deadline = entries['Deadline (YYYY-MM-DD)'].get()
            if not all([title, desc, loc, deadline]):
                messagebox.showerror("Error", "All fields required")
                return
            if company_ops.post_new_job(self.company_id, title, desc, cgpa, loc, deadline):
                messagebox.showinfo("Success", "Job posted!")
                for e in entries.values():
                    e.delete(0, tk.END)
                self.load_my_jobs()
            else:
                messagebox.showerror("Error", "Failed to post job")

        tk.Button(frame, text="Post Job", command=post, bg='#4CAF50', fg='white', font=("Arial", 12), padx=20).grid(row=len(fields), column=0, columnspan=2, pady=20)

    def load_applicants(self):
        for widget in self.applicants_tab.winfo_children():
            widget.destroy()
        apps = company_ops.get_applicants_for_company(self.company_id)
        if not apps:
            tk.Label(self.applicants_tab, text="No applications received.", font=("Arial", 14), bg='#ffffff').pack(pady=50)
            return
        columns = ['APPLICATION_ID', 'NAME', 'EMAIL', 'CGPA', 'JOB_TITLE', 'STATUS']
        tree = ttk.Treeview(self.applicants_tab, columns=columns, show='headings', height=15)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        tree.pack(fill='both', expand=True, padx=10, pady=10)
        for app in apps:
            tree.insert('', tk.END, values=(app['APPLICATION_ID'], app['NAME'], app['EMAIL'], app['CGPA'], app['JOB_TITLE'], app['STATUS']))

        def update_status():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Select an application")
                return
            app_id = tree.item(selected[0])['values'][0]
            new_status = status_var.get()
            if company_ops.update_application_status(app_id, new_status):
                messagebox.showinfo("Success", f"Status updated to {new_status}")
                self.load_applicants()
            else:
                messagebox.showerror("Error", "Update failed")

        status_frame = tk.Frame(self.applicants_tab, bg='#ffffff')
        status_frame.pack(pady=10)
        tk.Label(status_frame, text="Change Status to:", bg='#ffffff').pack(side='left', padx=5)
        status_var = tk.StringVar(value="Shortlisted")
        status_menu = ttk.Combobox(status_frame, textvariable=status_var, values=["Pending", "Shortlisted", "Selected", "Rejected"], state="readonly", width=12)
        status_menu.pack(side='left', padx=5)
        tk.Button(status_frame, text="Update", command=update_status, bg='#FF9800', fg='white').pack(side='left', padx=5)
        tk.Button(self.applicants_tab, text="Refresh", command=self.load_applicants, bg='#2196F3', fg='white').pack(pady=5)
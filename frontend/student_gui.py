import tkinter as tk
from tkinter import ttk, messagebox
from backend import student_ops
from utils.helpers import center_window, export_to_csv

class StudentDashboard:
    def __init__(self, student_id):
        self.student_id = student_id
        self.window = tk.Tk()
        self.window.title(f"Student Dashboard - {student_id}")
        center_window(self.window, 900, 650)
        self.window.configure(bg='#e8f4f8')

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook.Tab', font=('Arial', 10, 'bold'), padding=[10, 5])

        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Tab 1: Profile
        self.profile_tab = tk.Frame(self.notebook, bg='#ffffff')
        self.notebook.add(self.profile_tab, text="👤 My Profile")
        self.load_profile()

        # Tab 2: Available Jobs
        self.jobs_tab = tk.Frame(self.notebook, bg='#ffffff')
        self.notebook.add(self.jobs_tab, text="💼 Available Jobs")
        self.load_available_jobs()

        # Tab 3: My Applications
        self.apps_tab = tk.Frame(self.notebook, bg='#ffffff')
        self.notebook.add(self.apps_tab, text="📋 My Applications")
        self.load_my_applications()

        self.window.mainloop()

    def load_profile(self):
        for widget in self.profile_tab.winfo_children():
            widget.destroy()
        student_data = student_ops.get_student_details(self.student_id)
        if not student_data:
            messagebox.showerror("Error", "Could not load profile")
            return

        frame = tk.Frame(self.profile_tab, bg='#ffffff', padx=30, pady=30)
        frame.pack(fill='both', expand=True)

        labels = ["Student ID:", "Name:", "Email:", "Phone:", "Department:", "CGPA:", "Graduation Year:", "Skills:"]
        keys = ['STUDENT_ID', 'NAME', 'EMAIL', 'PHONE', 'DEPARTMENT', 'CGPA', 'GRADUATION_YEAR', 'SKILLS']
        for i, (label, key) in enumerate(zip(labels, keys)):
            tk.Label(frame, text=label, font=("Arial", 12, "bold"), bg='#ffffff', anchor='e').grid(row=i, column=0, sticky='e', padx=10, pady=8)
            tk.Label(frame, text=student_data.get(key, 'N/A'), font=("Arial", 12), bg='#ffffff', anchor='w').grid(row=i, column=1, sticky='w', padx=10, pady=8)

    def load_available_jobs(self):
        for widget in self.jobs_tab.winfo_children():
            widget.destroy()
        jobs = student_ops.get_available_jobs()
        if not jobs:
            tk.Label(self.jobs_tab, text="No jobs available.", font=("Arial", 14), bg='#ffffff').pack(pady=50)
            return

        # Treeview
        columns = ('JOB_ID', 'JOB_TITLE', 'COMPANY_NAME', 'REQUIRED_CGPA', 'LOCATION')
        tree = ttk.Treeview(self.jobs_tab, columns=columns, show='headings', height=15)
        tree.heading('JOB_ID', text='Job ID')
        tree.heading('JOB_TITLE', text='Title')
        tree.heading('COMPANY_NAME', text='Company')
        tree.heading('REQUIRED_CGPA', text='Req. CGPA')
        tree.heading('LOCATION', text='Location')
        tree.column('JOB_ID', width=80)
        tree.column('JOB_TITLE', width=200)
        tree.column('COMPANY_NAME', width=150)
        tree.column('REQUIRED_CGPA', width=80)
        tree.column('LOCATION', width=100)
        tree.pack(fill='both', expand=True, padx=10, pady=10)

        for job in jobs:
            tree.insert('', tk.END, values=(job['JOB_ID'], job['JOB_TITLE'], job['COMPANY_NAME'], job['REQUIRED_CGPA'], job['LOCATION']))

        # Buttons
        btn_frame = tk.Frame(self.jobs_tab, bg='#ffffff')
        btn_frame.pack(pady=10)

        def apply():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Select a job to apply.")
                return
            job_id = tree.item(selected[0])['values'][0]
            if student_ops.apply_for_job(self.student_id, job_id):
                messagebox.showinfo("Success", "Application submitted!")
                self.load_my_applications()  # refresh
            else:
                messagebox.showerror("Error", "Failed to apply. Already applied or database error.")

        tk.Button(btn_frame, text="Apply for Selected Job", command=apply, bg='#4CAF50', fg='white', font=("Arial", 11), padx=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Refresh Jobs", command=self.load_available_jobs, bg='#2196F3', fg='white', font=("Arial", 11), padx=15).pack(side='left', padx=5)

    def load_my_applications(self):
        for widget in self.apps_tab.winfo_children():
            widget.destroy()
        apps = student_ops.get_my_applications(self.student_id)
        if not apps:
            tk.Label(self.apps_tab, text="No applications found.", font=("Arial", 14), bg='#ffffff').pack(pady=50)
            return

        columns = ('APPLICATION_ID', 'JOB_TITLE', 'COMPANY_NAME', 'STATUS')
        tree = ttk.Treeview(self.apps_tab, columns=columns, show='headings', height=15)
        tree.heading('APPLICATION_ID', text='Application ID')
        tree.heading('JOB_TITLE', text='Job Title')
        tree.heading('COMPANY_NAME', text='Company')
        tree.heading('STATUS', text='Status')
        tree.column('APPLICATION_ID', width=120)
        tree.column('JOB_TITLE', width=200)
        tree.column('COMPANY_NAME', width=150)
        tree.column('STATUS', width=100)
        tree.pack(fill='both', expand=True, padx=10, pady=10)

        for app in apps:
            tree.insert('', tk.END, values=(app['APPLICATION_ID'], app['JOB_TITLE'], app['COMPANY_NAME'], app['STATUS']))

        btn_frame = tk.Frame(self.apps_tab, bg='#ffffff')
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Refresh", command=self.load_my_applications, bg='#2196F3', fg='white', font=("Arial", 11), padx=15).pack()
import tkinter as tk
from tkinter import messagebox, ttk
from backend import tpo_ops, student_ops, company_ops
from frontend import tpo_gui, student_gui, company_gui
from utils.helpers import center_window

class LoginWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Placement Management System - Login")
        center_window(self.window, 500, 400)
        self.window.configure(bg='#f0f0f0')
        self.window.resizable(False, False)

        # Title
        title = tk.Label(self.window, text="Student Placement System", font=("Arial", 18, "bold"), bg='#f0f0f0', fg='#2c3e50')
        title.pack(pady=20)

        # Main frame
        frame = tk.Frame(self.window, bg='#ffffff', relief=tk.RAISED, bd=2)
        frame.pack(padx=30, pady=20, fill='both', expand=True)

        # Username
        tk.Label(frame, text="Username:", font=("Arial", 12), bg='#ffffff').grid(row=0, column=0, padx=15, pady=15, sticky='e')
        self.username_entry = tk.Entry(frame, font=("Arial", 12), width=25)
        self.username_entry.grid(row=0, column=1, padx=15, pady=15)

        # Password
        tk.Label(frame, text="Password:", font=("Arial", 12), bg='#ffffff').grid(row=1, column=0, padx=15, pady=15, sticky='e')
        self.password_entry = tk.Entry(frame, font=("Arial", 12), width=25, show="*")
        self.password_entry.grid(row=1, column=1, padx=15, pady=15)

        # Role
        tk.Label(frame, text="Role:", font=("Arial", 12), bg='#ffffff').grid(row=2, column=0, padx=15, pady=15, sticky='e')
        self.role_var = tk.StringVar(value="Student")
        role_menu = ttk.Combobox(frame, textvariable=self.role_var, values=["Student", "Company", "TPO"], state="readonly", font=("Arial", 12))
        role_menu.grid(row=2, column=1, padx=15, pady=15, sticky='w')

        # Buttons frame
        btn_frame = tk.Frame(frame, bg='#ffffff')
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)

        login_btn = tk.Button(btn_frame, text="Login", command=self.authenticate, font=("Arial", 12, "bold"), bg='#4CAF50', fg='white', padx=20, width=12)
        login_btn.pack(side='left', padx=10)

        clear_btn = tk.Button(btn_frame, text="Clear", command=self.clear_fields, font=("Arial", 12), bg='#f44336', fg='white', padx=20, width=12)
        clear_btn.pack(side='left', padx=10)

        # Bind Enter key
        self.password_entry.bind('<Return>', lambda event: self.authenticate())
        self.username_entry.bind('<Return>', lambda event: self.authenticate())

    def clear_fields(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def authenticate(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        role = self.role_var.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return

        if role == "TPO":
            if tpo_ops.authenticate_tpo(username, password):
                self.window.destroy()
                tpo_gui.TPODashboard()
            else:
                messagebox.showerror("Error", "Invalid TPO credentials")
        elif role == "Student":
            if student_ops.authenticate_student(username, password):
                self.window.destroy()
                student_gui.StudentDashboard(username)
            else:
                messagebox.showerror("Error", "Invalid Student credentials")
        elif role == "Company":
            if company_ops.authenticate_company(username, password):
                self.window.destroy()
                company_gui.CompanyDashboard(username)
            else:
                messagebox.showerror("Error", "Invalid Company credentials")

    def run(self):
        self.window.mainloop()
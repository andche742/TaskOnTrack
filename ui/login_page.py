import tkinter as tk
from tkinter import ttk 
from controllers.user_controller import user_controller

class LoginPage(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.user_controller = user_controller

        center = ttk.Frame(self, padding= 40)
        center.pack(expand=True)

        # Introduction Label
        ttk.Label(
            center,
            text= "Welcome to TaskOnTrack!",
            font= ("Segoe UI", 20, "bold"),
        ).pack(pady=(0, 5))

        ttk.Label(
            center,
            text= "Your tasks, your pace, your progress.",
            font= ("Segoe UI", 11),
        ).pack(pady=(0, 20))

        # Username Entry
        ttk.Label(center, text="Username").pack(anchor="w")
        self.entry_username = ttk.Entry(center, width=30)
        self.entry_username.pack(pady=(0, 10))

        # Password Entry
        ttk.Label(center, text="Password").pack(anchor="w")
        self.entry_password = ttk.Entry(center, width=30, show="*")
        self.entry_password.pack(pady=(0, 20))

        # Login and Create Account Buttons
        btn_row = ttk.Frame(center)
        btn_row.pack()

        ttk.Button(
            btn_row,
            text="Login",
            command=self.on_login,
        ).grid(row=0, column=0, padx=10)

        ttk.Button(
            btn_row,
            text="Create account",
            command=self.on_create,
        ).grid(row=0, column=1, padx=10)

        self.output_text = tk.StringVar()
        self.output = ttk.Label(
            center,
            textvariable=self.output_text,
            foreground='red', # Placeholder for error messages
            font=("Segoe UI", 12, "italic"),
        ).pack(pady=(10, 0))

    def validate_inputs(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if not username or not password:
            self.output_text.set("Please enter both username and password")
            return None, None
        return username, password
    
    def on_login(self):
        username, password = self.validate_inputs()
        if not username:
            return

        success, result = self.user_controller.login(username, password) 

        if success:
            print("Login successful")
            self.app.show_frame("DashboardPage")
        else:
            print("Login failed")
            self.output_text.set(result)

    def on_create(self):
        username, password = self.validate_inputs()
        if not username:
            return
        
        success, result = self.user_controller.create_account(username, password)

        if success:
            print("Account creation successful")
            self.app.show_frame("DashboardPage")
        else:
            print("Account creation failed")
            self.output_text.set(result)

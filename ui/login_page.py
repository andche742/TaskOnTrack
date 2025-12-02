import tkinter as tk
from tkinter import ttk 
from controllers.user_controller import user_controller

class LoginPage(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.user_controller = user_controller

        # main card centered
        card = ttk.Frame(self, padding=40)
        card.pack(expand=True)
        card.columnconfigure(0, weight=1)  # everything in one column

        # title
        ttk.Label(
            card,
            text="Welcome to TaskOnTrack!",
            font=("Helvetica", 20, "bold"),
        ).grid(row=0, column=0, pady=(0, 10))

        ttk.Label(
            card,
            text="Your tasks, your pace, your progress.",
            font=("Helvetica", 11),
        ).grid(row=1, column=0, pady=(0, 20))

        # Username label + entry (stacked)
        ttk.Label(card, text="Username").grid(
            row=2, column=0, sticky="w", pady=(0, 3)
        )
        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(card, textvariable=self.username_var, width=30)
        self.username_entry.grid(row=3, column=0, sticky="ew", pady=(0, 10))

        # Password label + entry (stacked)
        ttk.Label(card, text="Password").grid(
            row=4, column=0, sticky="w", pady=(0, 3)
        )
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(
            card, textvariable=self.password_var, show="*", width=30
        )
        self.password_entry.grid(row=5, column=0, sticky="ew", pady=(0, 15))

        # Buttons row directly under the text boxes
        btn_row = ttk.Frame(card)
        btn_row.grid(row=6, column=0, pady=(0, 0))

        ttk.Button(
            btn_row,
            text="Login",
            width=12,
            command=self.on_login,
        ).grid(row=0, column=0, padx=5)

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
            self.app.current_user = result
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
            self.app.current_user = result
            self.app.show_frame("DashboardPage")
        else:
            print("Account creation failed")
            self.output_text.set(result)

import tkinter as tk
from tkinter import ttk 

class LoginPage(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

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

    def on_login(self):
        # username = self.entry_username.get()
        # password = self.entry_password.get()
        # self.app.authenticate_user(username, password) 
        self.app.show_frame("DashboardPage")


    def on_create(self):
        self.app.show_frame("DashboardPage")
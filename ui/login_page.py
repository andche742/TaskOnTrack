import tkinter as tk
from tkinter import ttk, messagebox


class LoginPage(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

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
            width=15,
            command=self.on_create_account,
        ).grid(row=0, column=1, padx=5)

        self.username_entry.focus_set()

    # simple validation / navigation handlers

    def _basic_validate(self) -> bool:
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()

        if not username or not password:
            messagebox.showwarning(
                "Missing information",
                "Please enter both username and password.",
            )
            return False
        return True

    def on_login(self):
        if not self._basic_validate():
            return
        self.app.current_user = self.username_var.get().strip()
        self.app.show_frame("DashboardPage")

    def on_create_account(self):
        if not self._basic_validate():
            return

        username = self.username_var.get().strip()
        messagebox.showinfo(
            "Account created",
            f"Account for '{username}' created (demo only).\nLogging you in...",
        )
        self.app.current_user = username
        self.app.show_frame("DashboardPage")

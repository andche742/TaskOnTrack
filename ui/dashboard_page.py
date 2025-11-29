from tkinter import ttk


class DashboardPage(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        container = ttk.Frame(self, padding=20)
        container.pack(expand=True, fill="both")

        ttk.Label(container, text="Dashboard (placeholder)", font=("Helvetica", 18, "bold")).pack(pady=10)
        ttk.Button(container, text="Back to login",
                   command=lambda: app.show_frame("LoginPage")).pack(pady=10)

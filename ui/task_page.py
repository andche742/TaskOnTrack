from tkinter import ttk


class TaskPage(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        ttk.Label(self, text="Task List (placeholder)").pack(pady=20)

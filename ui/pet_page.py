from tkinter import ttk


class PetPage(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        ttk.Label(self, text="Virtual Pet (placeholder)").pack(pady=20)
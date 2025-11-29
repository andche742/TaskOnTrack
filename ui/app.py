import tkinter as tk
from tkinter import ttk

from ui.login_page import LoginPage
from ui.dashboard_page import DashboardPage
from ui.task_page import TaskPage
from ui.pet_page import PetPage


class TaskOnTrackApp(tk.Tk):
    """Main Tkinter window that manages all pages."""

    def __init__(self):
        super().__init__()

        self.title("TaskOnTrack")
        self.geometry("900x600")
        self.resizable(False, False)

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.frames = {}

        for PageClass in (LoginPage, DashboardPage, TaskPage, PetPage):
            page_name = PageClass.__name__
            frame = PageClass(parent=container, app=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name: str):
        frame = self.frames[page_name]
        frame.tkraise()

import tkinter as tk
from tkinter import ttk

from ui.login_page import LoginPage
from ui.dashboard_page import DashboardPage
from ui.task_page import TaskPage
from ui.pet_page import PetPage


class TaskOnTrackApp(tk.Tk):

    def __init__(self):
        super().__init__()

        # window
        self.title("TaskOnTrack")
        self.geometry("900x600")
        self.resizable(False, False)

        # theme
        self.style = ttk.Style(self)
        self.current_theme = "light"
        self._apply_theme()  # set initial colors
        
        # placeholder user
        self.current_user = None

        # main container
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        # page frames
        self.frames = {}

        for PageClass in (LoginPage, DashboardPage, TaskPage, PetPage):
            page_name = PageClass.__name__
            frame = PageClass(parent=container, app=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # always start on login page
        self.show_frame("LoginPage")

    def show_frame(self, page_name: str):
        frame = self.frames[page_name]
        frame.tkraise()
        
        if hasattr(frame, 'refresh'):
            frame.refresh()

    def set_theme(self, mode: str):
        if mode not in ("light", "dark"):
            return
        self.current_theme = mode
        self._apply_theme()

    def _apply_theme(self):
        if self.current_theme == "light":
            bg = "#f5f5f5"
            fg = "#000000"
            accent = "#e5ddff"
        else:  # dark mode
            bg = "#202124"
            fg = "#ffffff"
            accent = "#3b3b70"

        # base tk window
        self.configure(bg=bg)

        # ttk base styles
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass

        self.style.configure("TFrame", background=bg)
        self.style.configure("TLabel", background=bg, foreground=fg)
        self.style.configure("TButton", foreground=fg)
        self.style.map("TButton", background=[("active", accent)])
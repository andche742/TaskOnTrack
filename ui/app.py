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

        # --- theme setup ---
        self.style = ttk.Style(self)
        self.current_theme = "light"
        self._apply_theme()  # set initial colors
        
        # Initialize current_user to None (will be set after login)
        self.current_user = None

        # Main container that holds all pages
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        # Store all page frames here
        self.frames = {}

        # Only these four pages for now
        for PageClass in (LoginPage, DashboardPage, TaskPage, PetPage):
            page_name = PageClass.__name__
            frame = PageClass(parent=container, app=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show Login first
        self.show_frame("LoginPage")

    def show_frame(self, page_name: str):
        """Raise the page with the given class name."""
        frame = self.frames[page_name]
        frame.tkraise()
        
        if hasattr(frame, 'refresh'):
            frame.refresh()

    # THEME CONTROL

    def set_theme(self, mode: str):
        """Public method pages can call to switch theme."""
        if mode not in ("light", "dark"):
            return
        self.current_theme = mode
        self._apply_theme()

    def _apply_theme(self):
        """Apply light or dark colors to the app."""
        if self.current_theme == "light":
            bg = "#f5f5f5"
            fg = "#000000"
            accent = "#e5ddff"  # soft purple
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
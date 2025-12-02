import tkinter as tk
from tkinter import ttk


class DashboardPage(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # --- layout grid for this page ---
        self.columnconfigure(0, weight=0)   # side nav
        self.columnconfigure(1, weight=1)   # main content
        self.rowconfigure(0, weight=1)

        # SIDE NAV (left)

        side_nav = ttk.Frame(self, padding=(20, 20))
        side_nav.grid(row=0, column=0, sticky="nsw")

        ttk.Label(
            side_nav,
            text="TaskOnTrack",
            font=("Helvetica", 18, "bold"),
        ).pack(anchor="w", pady=(0, 20))

        # Menu buttons
        ttk.Button(
            side_nav,
            text="Home",
            command=lambda: app.show_frame("DashboardPage"),
            width=12,
        ).pack(anchor="w", pady=4)

        ttk.Button(
            side_nav,
            text="Tasks",
            command=lambda: app.show_frame("TaskPage"),
            width=12,
        ).pack(anchor="w", pady=4)

        ttk.Button(
            side_nav,
            text="Rewards",
            command=lambda: app.show_frame("PetPage"),
            width=12,
        ).pack(anchor="w", pady=4)

        ttk.Button(
            side_nav,
            text="Settings",
            command=self.open_settings_dialog,
            width=12,
        ).pack(anchor="w", pady=4)


        # MAIN CONTENT AREA
   
        main = ttk.Frame(self, padding=(10, 20, 20, 20))
        main.grid(row=0, column=1, sticky="nsew")
        main.columnconfigure(0, weight=1)

        # Today Tasks board
        tasks_board = ttk.LabelFrame(main, text="Today Tasks", padding=10)
        tasks_board.grid(row=0, column=0, sticky="nsew")
        tasks_board.rowconfigure(0, weight=1)
        tasks_board.columnconfigure(0, weight=1)

        ttk.Label(
            tasks_board,
            text="(Tasks for today will appear here.)",
            font=("Helvetica", 11),
        ).grid(row=0, column=0, sticky="n")

        # Reward points display
        rewards_row = ttk.Frame(main)
        rewards_row.grid(row=1, column=0, sticky="ew", pady=(15, 0))
        rewards_row.columnconfigure(0, weight=1)
        rewards_row.columnconfigure(1, weight=1)

        self.today_points_var = tk.StringVar(value="Today Reward Points: 0 points")
        self.total_points_var = tk.StringVar(value="Total Reward Points: 0 points")

        ttk.Label(
            rewards_row,
            textvariable=self.today_points_var,
            padding=10,
            relief="groove",
        ).grid(row=0, column=0, sticky="ew", padx=(0, 8))

        ttk.Label(
            rewards_row,
            textvariable=self.total_points_var,
            padding=10,
            relief="groove",
        ).grid(row=0, column=1, sticky="ew", padx=(8, 0))

        # Pet mood + Feed button 
        pet_row = ttk.Frame(main)
        pet_row.grid(row=2, column=0, sticky="ew", pady=(15, 0))
        pet_row.columnconfigure(0, weight=3)
        pet_row.columnconfigure(1, weight=1)

        self.pet_mood_var = tk.StringVar(value="Pet Mood: normal")

        ttk.Label(
            pet_row,
            textvariable=self.pet_mood_var,
            padding=10,
            relief="groove",
        ).grid(row=0, column=0, sticky="ew", padx=(0, 8))

        ttk.Button(
            pet_row,
            text="Feed",
            command=self.on_feed_clicked,
        ).grid(row=0, column=1, sticky="e", padx=(8, 0))


    #  Handlers

    def on_feed_clicked(self):
        """
        TEMP behavior:
        For now just change the mood text.
        Later we will call PetController.add_points() and update mood from DB.
        """
        self.pet_mood_var.set("Pet Mood: happy")
        # example of updating today points visually
        self.today_points_var.set("Today Reward Points: 10 points")
        self.total_points_var.set("Total Reward Points: 10 points")

    def open_settings_dialog(self):
        """Open a small popup window for theme settings."""
        win = tk.Toplevel(self)
        win.title("Settings")
        win.transient(self.winfo_toplevel())  # tie to main window
        win.grab_set()  # make it modal-ish

        # Set a fixed small size
        win.geometry("300x160")

        container = ttk.Frame(win, padding=20)
        container.pack(expand=True, fill="both")

        ttk.Label(
            container,
            text="Theme",
            font=("Helvetica", 12, "bold"),
        ).pack(anchor="w", pady=(0, 10))

        # Buttons row
        row = ttk.Frame(container)
        row.pack(anchor="w", pady=(0, 10))

        ttk.Button(
            row,
            text="Light mode",
            width=12,
            command=lambda: self._set_theme_and_close(win, "light"),
        ).grid(row=0, column=0, padx=5)

        ttk.Button(
            row,
            text="Dark mode",
            width=12,
            command=lambda: self._set_theme_and_close(win, "dark"),
        ).grid(row=0, column=1, padx=5)

        ttk.Label(
            container,
            text="Choose theme for TaskOnTrack.",
            font=("Helvetica", 9),
        ).pack(anchor="w", pady=(10, 0))

    def _set_theme_and_close(self, win, mode: str):
        """Helper: change theme and close the popup."""
        self.app.set_theme(mode)
        win.destroy()


import tkinter as tk
from tkinter import ttk
from controllers.task_controller import task_controller
from controllers.user_controller import user_controller
from controllers.pet_controller import pet_controller

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

        # Scrollable frame for tasks checklist
        self.tasks_canvas = tk.Canvas(tasks_board, highlightthickness=0)
        scrollbar = ttk.Scrollbar(tasks_board, orient="vertical", command=self.tasks_canvas.yview)
        self.tasks_container = ttk.Frame(self.tasks_canvas)
        
        def update_scroll_region(event=None):
            self.tasks_canvas.configure(scrollregion=self.tasks_canvas.bbox("all"))
        
        self.tasks_container.bind("<Configure>", update_scroll_region)
        
        self.tasks_canvas.create_window((0, 0), window=self.tasks_container, anchor="nw")
        self.tasks_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.tasks_canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.task_checkboxes = {}

        self.total_points_var = tk.StringVar(value="")

        ttk.Label(
            main,
            textvariable=self.total_points_var,
            padding=10,
            relief="groove",
        ).grid(row=1, column=0, sticky="ew", padx=(8, 0))

        pet_row = ttk.Frame(main)
        pet_row.grid(row=2, column=0, sticky="ew", pady=(15, 0))
        pet_row.columnconfigure(0, weight=3)
        pet_row.columnconfigure(1, weight=1)

        self.pet_mood_var = tk.StringVar(value="Pet Mood: normal")
        if hasattr(self.app, 'current_user') and self.app.current_user is not None:
            self.pet_mood_var.set(pet_controller.get_mood(self.app.current_user.id))

        ttk.Label(
            pet_row,
            textvariable=self.pet_mood_var,
            padding=10,
            relief="groove",
        ).grid(row=0, column=0, sticky="ew", padx=(0, 8))

        self.load_today_tasks()

    #  Handlers

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
    
    def load_today_tasks(self):
        for widget in self.tasks_container.winfo_children():
            widget.destroy()
        self.task_checkboxes.clear()
        
        if not hasattr(self.app, 'current_user') or self.app.current_user is None:
            return
        
        user_id = self.app.current_user.id
        success, result = task_controller.get_tasks_for_today(user_id)
        
        if not success:
            print(result)
            return
        
        if not result:
            print("No tasks for today!")
            return
            
        for task in result:
            checked = tk.BooleanVar(value=(task.status == "complete"))
            checkbox = ttk.Checkbutton(
                self.tasks_container,
                text=f"{task.title} - {task.description}",
                variable=checked,
                command=lambda t=task, c=checked: self._on_task_toggle(t, c)
            )
            checkbox.pack(anchor="w", pady=2)
            self.task_checkboxes[task.id] = (checkbox, checked, task)
        
        self.tasks_canvas.update_idletasks()
        self.tasks_canvas.configure(scrollregion=self.tasks_canvas.bbox("all"))
    
    def _on_task_toggle(self, task, checked_var):
        if not hasattr(self.app, 'current_user') or self.app.current_user is None:
            return
            
        if checked_var.get():
            new_status = "complete"
            user_controller.add_points(self.app.current_user.id, 10)
        if not checked_var.get():
            new_status = "incomplete"
            user_controller.add_points(self.app.current_user.id, -10)

        task_controller.edit_task(task.id, status=new_status)
        self.total_points_var.set(f"Total Reward Points: {user_controller.get_points(self.app.current_user.id)} points")

    
    def refresh(self):
        self.load_today_tasks()
        if hasattr(self.app, 'current_user') and self.app.current_user is not None:
            self.total_points_var.set(f"Total Reward Points: {user_controller.get_points(self.app.current_user.id)} points")
        else:
            self.total_points_var.set("Total Reward Points: 0 points")


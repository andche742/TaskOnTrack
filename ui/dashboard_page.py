import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from controllers.task_controller import task_controller
from controllers.user_controller import user_controller
from controllers.pet_controller import pet_controller

class DashboardPage(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # layout grid
        self.columnconfigure(0, weight=0)   # side nav
        self.columnconfigure(1, weight=1)   # main content
        self.rowconfigure(0, weight=1)

        # side nav
        side_nav = ttk.Frame(self, padding=(20, 20))
        side_nav.grid(row=0, column=0, sticky="nsw")

        ttk.Label(
            side_nav,
            text="TaskOnTrack",
            font=("Helvetica", 18, "bold"),
        ).pack(anchor="w", pady=(0, 20))

        # nav buttons
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


        # main content
   
        main = ttk.Frame(self, padding=(10, 20, 20, 20))
        main.grid(row=0, column=1, sticky="nsew")
        main.columnconfigure(0, weight=1)

        # todays tasks
        tasks_board = ttk.LabelFrame(main, text="Today Tasks", padding=10)
        tasks_board.grid(row=0, column=0, sticky="nsew", pady=(0, 15))
        tasks_board.rowconfigure(0, weight=1)
        tasks_board.columnconfigure(0, weight=1)

        self.tasks_canvas = tk.Canvas(tasks_board, highlightthickness=0)
        scrollbar = ttk.Scrollbar(tasks_board, orient="vertical", command=self.tasks_canvas.yview)
        self.tasks_container = ttk.Frame(self.tasks_canvas)
        
        def update_scroll_region(event=None):
            self.tasks_canvas.configure(scrollregion=self.tasks_canvas.bbox("all"))
        
        self.tasks_container.bind("<Configure>", update_scroll_region)
        
        canvas_window = self.tasks_canvas.create_window((0, 0), window=self.tasks_container, anchor="nw")
        self.tasks_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.tasks_canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        def configure_canvas_width(event):
            canvas_width = event.width
            self.tasks_canvas.itemconfig(canvas_window, width=canvas_width)
        self.tasks_canvas.bind('<Configure>', configure_canvas_width)
        
        self.task_checkboxes = {}

        self.total_points_var = tk.StringVar(value="")

        ttk.Label(
            main,
            textvariable=self.total_points_var,
            padding=10,
            relief="groove",
        ).grid(row=1, column=0, sticky="ew", pady=(0, 15))

        pet_row = ttk.Frame(main)
        pet_row.grid(row=2, column=0, sticky="ew")
        pet_row.columnconfigure(0, weight=1)
        pet_row.columnconfigure(1, weight=3)

        # pet image
        self.pet_image_label = ttk.Label(pet_row)
        self.pet_image_label.grid(row=0, column=0, padx=(0, 10), sticky="w")

        # pet mood
        self.pet_mood_var = tk.StringVar(value="Pet Mood: normal")
        if hasattr(self.app, 'current_user') and self.app.current_user is not None:
            mood = pet_controller.get_mood(self.app.current_user.id)
            self.pet_mood_var.set(f"Pet Mood: {mood}")
            self.update_pet_image(mood)
        else:
            self.update_pet_image("normal")
        
        ttk.Label(
            pet_row,
            textvariable=self.pet_mood_var,
            padding=10,
            relief="groove",
        ).grid(row=0, column=1, sticky="ew")

        self.load_today_tasks()

    def open_settings_dialog(self):
        win = tk.Toplevel(self)
        win.title("Settings")
        win.transient(self.winfo_toplevel()) 
        win.grab_set() 
        win.geometry("300x160")

        container = ttk.Frame(win, padding=20)
        container.pack(expand=True, fill="both")

        ttk.Label(
            container,
            text="Theme",
            font=("Helvetica", 12, "bold"),
        ).pack(anchor="w", pady=(0, 10))

        # light/dark buttons
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
    
    def _on_task_toggle(self, task, checked_var): # called when a task checkbox is toggled
        if not hasattr(self.app, 'current_user') or self.app.current_user is None:
            return
            
        if checked_var.get():
            new_status = "complete"
            user_controller.add_points(self.app.current_user.id, 10)
        if not checked_var.get():
            new_status = "incomplete"
            user_controller.add_points(self.app.current_user.id, -10)

        task_controller.edit_task(task.id, status=new_status)
        self.total_points_var.set(f"Reward Points: {user_controller.get_points(self.app.current_user.id)} points")

    
    def update_pet_image(self, mood):
        mood_to_image = {
            "normal": "pet_happy.png",
            "hungry": "pet_hungry.png",
            "bored": "pet_bored.png",
            "sad": "pet_sad.png",
        }
        
        image_filename = mood_to_image.get(mood.lower(), "pet_happy.png")
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "assets", image_filename)
        
        try:
            image = Image.open(image_path)
            image = image.resize((250, 250), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            
            self.pet_image_label.configure(image=photo)
            self.pet_image_label.image = photo 
        except Exception as e:
            print(f"Error loading pet image: {e}")
    
    def refresh(self):
        self.load_today_tasks()
        if hasattr(self.app, 'current_user') and self.app.current_user is not None:
            self.total_points_var.set(f"Reward Points: {user_controller.get_points(self.app.current_user.id)} points")
            
            result = pet_controller.update_pet_over_time(self.app.current_user.id)
            if result[0]:  # Success
                pet = result[1]
                mood = pet.mood
            else:
                print(f"Pet update failed: {result[1]}")
                mood = pet_controller.get_mood(self.app.current_user.id)
            
            self.pet_mood_var.set(f"Pet Mood: {mood}")
            self.update_pet_image(mood)
        else:
            self.total_points_var.set("Reward Points: 0 points")
            self.update_pet_image("normal")


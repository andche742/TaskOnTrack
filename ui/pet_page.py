import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk
from controllers.pet_controller import pet_controller
from controllers.user_controller import user_controller


class PetPage(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        self.mood_var = tk.StringVar(value="Pet Mood: normal") # defaults
        self.points_var = tk.StringVar(value="Reward Points: 0")

        # main content
        container = ttk.Frame(self, padding=20)
        container.pack(expand=True, fill="both")
        container.columnconfigure(0, weight=1)

        # title
        top_row = ttk.Frame(container)
        top_row.pack(fill="x")

        ttk.Label(
            top_row,
            text="Virtual Pet",
            font=("Helvetica", 18, "bold"),
        ).pack(side="left")

        # home button
        ttk.Button(
            top_row,
            text="Back to Dashboard",
            command=lambda: app.show_frame("DashboardPage"),
        ).pack(side="right")

        pet_frame = ttk.Frame(container, relief="ridge", padding=10)
        pet_frame.pack(pady=(20, 10))

        pet_frame.config(width=500, height=300)
        pet_frame.pack_propagate(False)

        self.pet_label = ttk.Label(pet_frame)
        self.pet_label.place(relx=0.5, rely=0.5, anchor="center")

        info_row = ttk.Frame(container)
        info_row.pack(fill="x", pady=(10, 10))

        ttk.Label(
            info_row,
            textvariable=self.mood_var,
            padding=10,
            relief="groove",
        ).grid(row=0, column=0, sticky="ew", padx=(0, 8))

        ttk.Label(
            info_row,
            textvariable=self.points_var,
            padding=10,
            relief="groove",
        ).grid(row=0, column=1, sticky="ew", padx=(8, 0))

        info_row.columnconfigure(0, weight=1)
        info_row.columnconfigure(1, weight=1)

        # interaction buttons
        btn_row = ttk.Frame(container)
        btn_row.pack(pady=(0, 10))

        ttk.Button(btn_row, text="Feed", width=10, command=self.on_feed).grid(
            row=0, column=0, padx=8
        )
        ttk.Button(btn_row, text="Pat", width=10, command=self.on_pat).grid(
            row=0, column=1, padx=8
        )
        ttk.Button(btn_row, text="Play", width=10, command=self.on_play).grid(
            row=0, column=2, padx=8
        )

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
            
            self.pet_label.configure(image=photo)
            self.pet_label.image = photo
        except Exception as e:
            print(f"Error loading pet image: {e}")

    def refresh(self):
        """Refresh pet data from database."""
        if not hasattr(self.app, 'current_user') or self.app.current_user is None:
            self.mood_var.set("Pet Mood: normal")
            self.points_var.set("Reward Points: 0")
            self.update_pet_image("normal")
            return
        
        user_id = self.app.current_user.id
        
        # decay mood over time
        pet_controller.update_pet_over_time(user_id)
        
        mood = pet_controller.get_mood(user_id)
        self.mood_var.set(f"Pet Mood: {mood}")
        self.update_pet_image(mood)
        
        points = user_controller.get_points(user_id)
        self.points_var.set(f"Reward Points: {points} points")

    def on_feed(self):
        if not hasattr(self.app, 'current_user') or self.app.current_user is None:
            return
        
        user_id = self.app.current_user.id
        
        current_points = user_controller.get_points(user_id)
        if current_points < 10:
            print("Not enough points to feed pet!")
            return
        
        success, pet = pet_controller.update_pet_stats(user_id, hunger_change=50)
        
        if success:
            user_controller.add_points(user_id, -10)
            self.refresh()
        else:
            print(f"Error feeding pet: {pet}")

    def on_pat(self):
        if not hasattr(self.app, 'current_user') or self.app.current_user is None:
            return
        
        user_id = self.app.current_user.id
        
        current_points = user_controller.get_points(user_id)
        if current_points < 5:
            print("Not enough points to pat pet!")
            return
        
        success, pet = pet_controller.update_pet_stats(user_id, boredom_change=20)
        
        if success:
            user_controller.add_points(user_id, -5)
            self.refresh()
        else:
            print(f"Error patting pet: {pet}")

    def on_play(self):
        if not hasattr(self.app, 'current_user') or self.app.current_user is None:
            return
        
        user_id = self.app.current_user.id
        
        current_points = user_controller.get_points(user_id)
        if current_points < 10:
            print("Not enough points to play with pet!")
            return
        
        success, pet = pet_controller.update_pet_stats(user_id, boredom_change=40)
        
        if success:
            user_controller.add_points(user_id, -10)
            self.refresh()
        else:
            print(f"Error playing with pet: {pet}")

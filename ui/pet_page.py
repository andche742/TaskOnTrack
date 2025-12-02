import tkinter as tk
from tkinter import ttk
import os


class PetPage(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        self.points = 0
        self.mood_var = tk.StringVar(value="Pet Mood: hungry")
        self.points_var = tk.StringVar(value="Reward Points: 0")

        # MAIN CONTAINER
        container = ttk.Frame(self, padding=20)
        container.pack(expand=True, fill="both")
        container.columnconfigure(0, weight=1)

        # TITLE ROW 
        top_row = ttk.Frame(container)
        top_row.pack(fill="x")

        ttk.Label(
            top_row,
            text="Virtual Pet",
            font=("Helvetica", 18, "bold"),
        ).pack(side="left")

        ttk.Button(
            top_row,
            text="Back to Dashboard",
            command=lambda: app.show_frame("DashboardPage"),
        ).pack(side="right")

        # PET CARD AREA (like wireframe box)
        pet_frame = ttk.Frame(container, relief="ridge", padding=10)
        pet_frame.pack(pady=(20, 10))

        # fixed size so the card looks like the Figma box
        pet_frame.config(width=500, height=300)
        # do not let the frame resize itself to the image
        pet_frame.pack_propagate(False)

        #  LOAD & SCALE IMAGES 
        assets_dir = os.path.join(os.path.dirname(__file__), "assets")

        # try 3 or 4; bigger number = smaller image
        scale_factor = 3

        self.pet_images = {}
        for mood, filename in [
            ("hungry", "pet_hungry.png"),
            ("sad", "pet_sad.png"),
            ("happy", "pet_happy.png"),
        ]:
            img = tk.PhotoImage(file=os.path.join(assets_dir, filename))
            # shrink image by an integer factor
            img = img.subsample(scale_factor, scale_factor)
            self.pet_images[mood] = img

        self.current_mood = "hungry"

        # center the pet inside the fixed-size card
        self.pet_label = ttk.Label(pet_frame, image=self.pet_images[self.current_mood])
        self.pet_label.place(relx=0.5, rely=0.5, anchor="center")

        # INFO ROW (Mood + Points) 
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

        # BUTTON ROW (Feed / Pat / Play)
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

    # Handlers

    def _set_mood(self, mood: str, text: str, points_add: int):
        self.current_mood = mood
        self.mood_var.set(f"Pet Mood: {text}")
        self.points += points_add
        self.points_var.set(f"Reward Points: {self.points}")
        self.pet_label.configure(image=self.pet_images[mood])

    def on_feed(self):
        # hungry → happy
        self._set_mood("happy", "happy (Just ate!)", points_add=5)

    def on_pat(self):
        # sad → comforted
        self._set_mood("happy", "comforted (Huggie Hug!)", points_add=3)

    def on_play(self):
        # normal → playful
        self._set_mood("happy", "happy & playful", points_add=4)

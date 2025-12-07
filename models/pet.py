class Pet:
    def __init__(self, pet_id: int, user_id: int, mood: str, bored: int, hunger: int):
        self.id = pet_id
        self.user_id = user_id # id of owner
        self.hunger = hunger # 0-100 hunger stat for hunger mood
        self.mood = mood  # happy, hungry, bored, sad
        self.bored = bored # 0-100 bored stat for bored mood

    def __repr__(self) -> str:
        return (
            f"Pet(id={self.id}, user_id={self.user_id}, "
            f"mood={self.mood})"
            f"bored={self.bored})"
            f"hunger={self.hunger})"
        )
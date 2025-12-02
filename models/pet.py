class Pet:
    def __init__(self, pet_id: int, user_id: int, mood: str, bored: int, hunger: int):
        self.id = pet_id
        self.user_id = user_id
        self.hunger = hunger # 0-100
        self.mood = mood  # e.g. 'happy', 'hungry', 'bored', sad etc
        self.bored = bored # 0-100

    def __repr__(self) -> str:
        return (
            f"Pet(id={self.id}, user_id={self.user_id}, "
            f"mood={self.mood})"
            f"bored={self.bored})"
            f"hunger={self.hunger})"
        )
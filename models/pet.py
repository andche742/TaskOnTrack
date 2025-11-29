class Pet:
    def __init__(self, pet_id: int, user_id: int, points: int, mood: str):
        self.id = pet_id
        self.user_id = user_id
        self.points = points
        self.mood = mood  # e.g. 'happy', 'hungry', 'sleepy'

    def __repr__(self) -> str:
        return (
            f"Pet(id={self.id}, user_id={self.user_id}, "
            f"points={self.points}, mood={self.mood!r})"
        )
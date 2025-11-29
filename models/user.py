class User:
    def __init__(self, user_id: int, username: str, password: str):
        self.id = user_id
        self.username = username
        self.password = password  

    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username!r})"

class Task:
    """Represents a single task in the system."""

    def __init__(
        self,
        task_id: int,
        user_id: int,
        title: str,
        description: str,
        due_date: str,
        status: str,
    ):
        self.id = task_id
        self.user_id = user_id  # id of the user who owns the task
        self.title = title
        self.description = description
        self.due_date = due_date   
        self.status = status  # incomplete, complete

    def __repr__(self) -> str:
        return (
            f"Task(id={self.id}, user_id={self.user_id}, "
            f"title={self.title!r}, due_date={self.due_date!r}, "
            f"status={self.status!r})"
        )

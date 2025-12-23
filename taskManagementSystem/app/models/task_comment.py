from typing import TYPE_CHECKING
from uuid import uuid4

if TYPE_CHECKING:
    from app.models.task import Task
    from app.models.user import User

class TaskComment:
    def __init__(self, task: "Task", comment: str, author: "User"):
        self.id = str(uuid4())
        self.task = task
        self.comment = comment
        self.author = author

    def get_task(self) -> "Task":
        return self.task

    def get_comment(self) -> str:
        return self.comment

    def get_author(self) -> "User":
        return self.author
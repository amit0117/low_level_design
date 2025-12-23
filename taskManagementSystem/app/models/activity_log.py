from typing import TYPE_CHECKING
from datetime import datetime
from uuid import uuid4

if TYPE_CHECKING:
    from app.models.task import Task
    from app.models.user import User


class ActivityLog:
    def __init__(self, task: "Task", user: "User", activity: str):
        self.id = str(uuid4())
        self.task = task
        self.user = user
        self.activity = activity
        self.timestamp = datetime.now()

    def get_id(self) -> str:
        return self.id

    def get_task(self) -> "Task":
        return self.task

    def get_user(self) -> "User":
        return self.user

    def get_activity(self) -> str:
        return self.activity

    def get_timestamp(self) -> datetime:
        return self.timestamp

    def __str__(self) -> str:
        return f"ActivityLog(task={self.task}, user={self.user}, activity={self.activity}, timestamp={self.timestamp})"

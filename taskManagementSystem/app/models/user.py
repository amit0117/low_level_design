from uuid import uuid4
from app.observers.task import TaskObserver
from typing import TYPE_CHECKING
from app.models.enums import TaskStatus, TaskPriority, TaskTag

if TYPE_CHECKING:
    from app.models.task import Task
    from app.models.task_comment import TaskComment
    from app.models.activity_log import ActivityLog


class User(TaskObserver):
    def __init__(self, name: str, email: str):
        super().__init__()  # Initialize the TaskObserver
        self.id = str(uuid4())
        self.name = name
        self.email = email
        self.task_history: list["Task"] = []

    def get_id(self) -> str:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_email(self) -> str:
        return self.email

    def get_task_history(self) -> list["Task"]:
        return self.task_history

    def get_task_history_by_status(self, status: TaskStatus) -> list["Task"]:
        return [task for task in self.task_history if task.get_status() == status]

    def get_task_history_by_priority(self, priority: TaskPriority) -> list["Task"]:
        return [task for task in self.task_history if task.get_priority() == priority]

    def get_task_history_by_tags(self, tags: list[TaskTag]) -> list["Task"]:
        return [task for task in self.task_history if task.get_tags() == tags]

    def add_task_to_history(self, task: "Task") -> None:
        self.task_history.append(task)

    def remove_task_from_history(self, task: "Task") -> None:
        self.task_history.remove(task)

    def update_on_task_status_change(self, task: "Task") -> None:
        if task.get_status() == TaskStatus.COMPLETED:
            print(f"Task {task.get_title()} completed by the user {self.name}")
            # add to the activity log
            return
        print(f"User {self.name} notified about task {task.get_title()} status change to {task.get_status()}")

    def update_on_task_comment_added(self, task: "Task", comment: "TaskComment") -> None:
        print(f"User {self.name} notified about task {task.get_title()} comment added: {comment.get_comment()}")

    def update_on_task_activity_log_added(self, task: "Task", activity: "ActivityLog") -> None:
        print(f"User {self.name} notified about task {task.get_title()} activity log added: {activity.get_activity()}")

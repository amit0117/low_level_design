from typing import TYPE_CHECKING, Optional
from uuid import uuid4
from app.models.enums import TaskStatus, TaskPriority, TaskTag
from datetime import datetime
from threading import Lock

if TYPE_CHECKING:
    from app.models.task import Task
    from app.models.user import User


class TaskList:
    def __init__(self, name: str, created_by: "User", tasks: Optional[list["Task"]] = None):
        self.id = str(uuid4())
        self.name = name
        self.created_by = created_by
        self.sub_tasks: list["Task"] = tasks or []
        self.status: Optional[TaskStatus] = None
        self.created_at = datetime.now()
        self.lock = Lock()  # To ensure date integrity while updating the status and adding/removing tasks
        if tasks:
            for task in tasks:
                # Set the parent task id to the task list ID (not the object itself)
                task.set_parent_task_id(self.get_id())

    def get_id(self) -> str:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_created_by(self) -> "User":
        return self.created_by

    def get_created_at(self) -> datetime:
        return self.created_at

    def get_sub_tasks(self) -> list["Task"]:
        return self.sub_tasks

    def get_status(self) -> Optional[TaskStatus]:
        return self.status

    def set_status(self, status: TaskStatus) -> None:
        with self.lock:
            self.status = status

    def add_sub_task(self, task: "Task") -> None:
        with self.lock:
            # Set the parent task id to the task list
            task.set_parent_task_id(self.get_id())
            self.sub_tasks.append(task)

    def remove_sub_task(self, task: "Task") -> None:
        with self.lock:
            # Remove the parent task id from the task
            task.set_parent_task_id(None)
            self.sub_tasks.remove(task)

    def get_sub_task_by_id(self, task_id: str) -> Optional["Task"]:
        return next((task for task in self.sub_tasks if task.get_id() == task_id), None)

    def get_sub_task_by_title(self, title: str) -> Optional["Task"]:
        return next((task for task in self.sub_tasks if task.get_title() == title), None)

    def get_sub_tasks_by_status(self, status: TaskStatus) -> list["Task"]:
        return [task for task in self.sub_tasks if task.get_status() == status]

    def get_sub_tasks_by_priority(self, priority: TaskPriority) -> list["Task"]:
        return [task for task in self.sub_tasks if task.get_priority() == priority]

    def get_sub_tasks_by_tags(self, tags: list[TaskTag]) -> list["Task"]:
        return [task for task in self.sub_tasks if task.get_tags() == tags]

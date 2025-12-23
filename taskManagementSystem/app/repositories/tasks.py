from typing import Optional, TYPE_CHECKING
from threading import Lock
from app.models.enums import TaskStatus, TaskPriority, TaskTag

if TYPE_CHECKING:
    from app.models.task import Task
    from app.models.user import User
    from app.models.task_list import TaskList


class TaskRepository:
    _instance: Optional["TaskRepository"] = None
    _lock = Lock()

    def __new__(cls) -> "TaskRepository":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if hasattr(self, "tasks"):
            return
        self.process_lock = Lock()
        self.tasks: dict[str, "Task"] = dict()
        self.task_lists: dict[str, "TaskList"] = dict()  # Task lists are used to group tasks together

    @classmethod
    def get_instance(cls) -> "TaskRepository":
        return cls._instance or cls()

    def add_task(self, task: "Task") -> None:
        with self.process_lock:
            self.tasks[task.get_id()] = task

    def remove_task(self, task: "Task") -> None:
        with self.process_lock:
            if task.get_id() not in self.tasks:
                raise ValueError("Task not found")
            # Remove the task from the task list or parent task
            parent_id = task.get_parent_task_id()
            if parent_id:
                task_list = self.get_task_list_by_id(parent_id)
                if task_list:
                    task_list.remove_sub_task(task)

            # When this del is executed then the destructor of the task will be called
            # and it will remove the task from all the observers
            del self.tasks[task.get_id()]

    def get_task_by_id(self, task_id: str) -> Optional["Task"]:
        return self.tasks.get(task_id)

    def get_task_by_title(self, title: str) -> Optional["Task"]:
        return next((task for task in self.tasks.values() if task.get_title() == title), None)

    def get_tasks_by_status(self, status: TaskStatus) -> list["Task"]:
        return [task for task in self.tasks.values() if task.get_status() == status]

    def get_tasks_by_priority(self, priority: TaskPriority) -> list["Task"]:
        return [task for task in self.tasks.values() if task.get_priority() == priority]

    def get_tasks_by_tags(self, tags: list[TaskTag]) -> list["Task"]:
        return [task for task in self.tasks.values() if task.get_tags() and set(tags).issubset(set(task.get_tags()))]

    def get_tasks_by_assignee(self, user: "User") -> list["Task"]:
        return [task for task in self.tasks.values() if task.get_assignees() and user in task.get_assignees()]

    def get_tasks_by_creator(self, user: "User") -> list["Task"]:
        return [task for task in self.tasks.values() if task.get_created_by().get_id() == user.get_id()]

    def get_all_tasks(self) -> list["Task"]:
        return list(self.tasks.values())

    def update_task(self, task: "Task") -> None:
        with self.process_lock:
            if task.get_id() not in self.tasks:
                raise ValueError("Task not found")
            self.tasks[task.get_id()] = task

    def add_task_list(self, task_list: "TaskList") -> None:
        with self.process_lock:
            self.task_lists[task_list.get_id()] = task_list

    def remove_task_list(self, task_list: "TaskList") -> None:
        with self.process_lock:
            if task_list.get_id() not in self.task_lists:
                raise ValueError("Task list not found")
            del self.task_lists[task_list.get_id()]

    def get_task_list_by_id(self, task_list_id: str) -> Optional["TaskList"]:
        return self.task_lists.get(task_list_id)

    def get_task_list_by_name(self, name: str) -> Optional["TaskList"]:
        return next((task_list for task_list in self.task_lists.values() if task_list.get_name() == name), None)

    def get_task_lists_by_creator(self, user: "User") -> list["TaskList"]:
        return [task_list for task_list in self.task_lists.values() if task_list.get_created_by().get_id() == user.get_id()]

    def get_all_task_lists(self) -> list["TaskList"]:
        return list(self.task_lists.values())

    def update_task_list(self, task_list: "TaskList") -> None:
        with self.process_lock:
            if task_list.get_id() not in self.task_lists:
                raise ValueError("Task list not found")
            self.task_lists[task_list.get_id()] = task_list

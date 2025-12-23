from abc import ABC, abstractmethod
from app.models.task import Task
from typing import Any
from app.repositories.tasks import TaskRepository
from app.models.enums import TaskPriority, TaskStatus, TaskTag
from datetime import datetime
from app.models.user import User


class TaskSearchStrategy(ABC):
    def __init__(self):
        self.task_repository = TaskRepository.get_instance()

    @abstractmethod
    def search(self, query: Any) -> list[Task]:
        raise NotImplementedError("Subclasses must implement this method")


class TaskSearchByPriorityStrategy(TaskSearchStrategy):
    def search(self, query: TaskPriority) -> list[Task]:
        # return tasks by priority
        return sorted(self.task_repository.get_tasks_by_priority(query), key=lambda x: x.get_priority().value, reverse=True)


class TaskSearchByDueDateStrategy(TaskSearchStrategy):
    def search(self, query: datetime) -> list[Task]:
        # return tasks by due date (less than or equal to the query)
        return sorted(
            [task for task in self.task_repository.get_all_tasks() if task.get_due_date() <= query], key=lambda x: x.get_due_date(), reverse=True
        )


class TaskSearchByAssigneeStrategy(TaskSearchStrategy):
    def search(self, query: "User") -> list[Task]:
        return self.task_repository.get_tasks_by_assignee(query)


class TaskSearchByTagsStrategy(TaskSearchStrategy):
    def search(self, query: list[TaskTag]) -> list[Task]:
        return [task for task in self.task_repository.get_all_tasks() if any(tag in task.get_tags() for tag in query)]


class TaskSearchByStatusStrategy(TaskSearchStrategy):
    def search(self, query: TaskStatus) -> list[Task]:
        return self.task_repository.get_tasks_by_status(query)

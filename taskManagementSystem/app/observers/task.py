from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.task import Task
    from app.models.task_comment import TaskComment
    from app.models.activity_log import ActivityLog


class TaskObserver(ABC):
    @abstractmethod
    def update_on_task_status_change(self, task: "Task") -> None:
        raise NotImplementedError("update_on_task_status_change method has not been implemented")

    @abstractmethod
    def update_on_task_comment_added(self, task: "Task", comment: "TaskComment") -> None:
        raise NotImplementedError("update_on_task_comment_added method has not been implemented")

    @abstractmethod
    def update_on_task_activity_log_added(self, task: "Task", activity: "ActivityLog") -> None:
        raise NotImplementedError("update_on_task_activity_log_added method has not been implemented")


class TaskSubject:
    def __init__(self):
        self.observers: list[TaskObserver] = []

    def add_observer(self, observer: TaskObserver) -> None:
        self.observers.append(observer)

    def remove_observer(self, observer: TaskObserver) -> None:
        self.observers.remove(observer)

    def notify_observers_on_task_status_change(self, task: "Task") -> None:
        for observer in self.observers:
            observer.update_on_task_status_change(task)

    def notify_observers_on_task_comment_added(self, task: "Task", comment: "TaskComment") -> None:
        for observer in self.observers:
            observer.update_on_task_comment_added(task, comment)

    def notify_observers_on_task_activity_log_added(self, task: "Task", activity: "ActivityLog") -> None:
        for observer in self.observers:
            observer.update_on_task_activity_log_added(task, activity)

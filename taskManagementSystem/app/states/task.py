from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from app.models.enums import TaskStatus

if TYPE_CHECKING:
    from app.models.task import Task


# Task State changes: TODO -> IN_PROGRESS -> IN_REVIEW -> COMPLETED
class TaskState(ABC):

    @abstractmethod
    def start_progress(self, task: "Task") -> None:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def reopen_task(self, task: "Task") -> bool:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def submit_for_review(self, task: "Task") -> None:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def complete_task(self, task: "Task") -> None:
        raise NotImplementedError("Subclasses must implement this method")


class TodoState(TaskState):
    def start_progress(self, task: "Task") -> None:
        print(f"Task {task.get_title()} started progress from TODO state")
        task.set_status(TaskStatus.IN_PROGRESS)
        task.set_state(InProgressState())

    def submit_for_review(self, task: "Task") -> None:
        print("Invalid: Cannot submit task for review from TODO state. Start progress first.")

    def complete_task(self, task: "Task") -> None:
        print("Invalid: Cannot complete task from TODO state. Start progress and submit for review first.")

    def reopen_task(self, task: "Task") -> bool:
        print("Invalid: Task is already in TODO state.")
        return False


class InProgressState(TaskState):
    def start_progress(self, task: "Task") -> None:
        print("Invalid: Task is already in progress.")

    def submit_for_review(self, task: "Task") -> None:
        task.set_status(TaskStatus.IN_REVIEW)
        task.set_state(InReviewState())

    def complete_task(self, task: "Task") -> None:
        print("Invalid: Cannot complete task from IN_PROGRESS state. Submit for review first.")

    def reopen_task(self, task: "Task") -> bool:
        print("Invalid: Cannot reopen task from IN_PROGRESS state. Complete the task first or cancel the review.")
        return False


class InReviewState(TaskState):
    def start_progress(self, task: "Task") -> None:
        print("Invalid: Task is already in review. Cannot start progress again.")

    def submit_for_review(self, task: "Task") -> None:
        print("Invalid: Task is already submitted for review.")

    def complete_task(self, task: "Task") -> None:
        task.set_status(TaskStatus.COMPLETED)
        task.set_state(CompletedState())

    def reopen_task(self, task: "Task") -> bool:
        print("Invalid: Cannot reopen task from IN_REVIEW state. Complete or reject the review first.")
        return False


class CompletedState(TaskState):
    def start_progress(self, task: "Task") -> None:
        print("Invalid: Cannot start progress on a completed task. Reopen the task first.")

    def submit_for_review(self, task: "Task") -> None:
        print("Invalid: Cannot submit completed task for review. Reopen the task first.")

    def complete_task(self, task: "Task") -> None:
        print("Invalid: Task is already completed.")

    def reopen_task(self, task: "Task") -> bool:
        task.set_status(TaskStatus.TODO)
        task.set_state(TodoState())
        return True

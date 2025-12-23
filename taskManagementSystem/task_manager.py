# Task manager will have list of tasks (Single Task Entity)
# It will also have list of TaskLists (Tasks grouped together by some criteria like projects, etc)
# Why we didn't keep only TaskLists, because every task need not be a part of a project. Some tasks are standalone.
from threading import Lock
from typing import Optional
from datetime import datetime
from app.strategies.task_serarch import TaskSearchStrategy
from app.repositories.tasks import TaskRepository
from app.repositories.users import UserRepository
from app.models.user import User
from app.models.task import Task
from app.models.task_list import TaskList
from app.models.task_comment import TaskComment
from app.models.enums import TaskStatus, TaskPriority, TaskTag


class TaskManager:
    _instance: Optional["TaskManager"] = None
    _lock = Lock()

    def __new__(cls) -> "TaskManager":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._has_initialized = False
        return cls._instance

    def __init__(self) -> None:
        if self._has_initialized:
            return
        self.task_repository = TaskRepository.get_instance()
        self.user_repository = UserRepository.get_instance()
        self.task_search_strategies: Optional[TaskSearchStrategy] = None
        self._has_initialized = True

    @classmethod
    def get_instance(cls) -> "TaskManager":
        return cls._instance or cls()

    def add_task_search_strategy(self, strategy: TaskSearchStrategy) -> None:
        self.task_search_strategies = strategy

    def remove_task_search_strategy(self) -> None:
        self.task_search_strategies = None

    def search_tasks(self, query) -> list[Task]:
        if not self.task_search_strategies:
            raise ValueError("No search strategy set")
        return self.task_search_strategies.search(query)

    def create_user(self, name: str, email: str) -> User:
        existing_user = self.user_repository.get_user_by_email(email)
        if existing_user:
            raise ValueError(f"User with email {email} already exists")
        user = User(name, email)
        self.user_repository.add_user(user)
        return user

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        return self.user_repository.get_user_by_id(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.user_repository.get_user_by_email(email)

    def get_user_by_name(self, name: str) -> Optional[User]:
        return self.user_repository.get_user_by_name(name)

    def get_all_users(self) -> list[User]:
        return self.user_repository.get_all_users()

    def delete_user(self, user_id: str) -> None:
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        self.user_repository.remove_user(user)

    def _get_task_by_id_or_raise(self, task_id: str) -> Task:
        task = self.task_repository.get_task_by_id(task_id)
        if not task:
            raise ValueError("Task not found")
        return task

    def _get_task_list_by_id_or_raise(self, task_list_id: str) -> TaskList:
        task_list = self.task_repository.get_task_list_by_id(task_list_id)
        if not task_list:
            raise ValueError("Task list not found")
        return task_list

    def add_task(self, task: Task) -> None:
        if not self.user_repository.get_user_by_id(task.get_created_by().get_id()):
            raise ValueError("Creator user not found in repository")
        if task.get_assignees():
            for user in task.get_assignees():
                if not self.user_repository.get_user_by_id(user.get_id()):
                    raise ValueError(f"Assigned user {user.get_id()} not found in repository")
        self.task_repository.add_task(task)

    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        return self.task_repository.get_task_by_id(task_id)

    def get_task_by_title(self, title: str) -> Optional[Task]:
        return self.task_repository.get_task_by_title(title)

    def get_tasks_by_status(self, status: TaskStatus) -> list[Task]:
        return self.task_repository.get_tasks_by_status(status)

    def get_tasks_by_priority(self, priority: TaskPriority) -> list[Task]:
        return self.task_repository.get_tasks_by_priority(priority)

    def get_tasks_by_tags(self, tags: list[TaskTag]) -> list[Task]:
        return self.task_repository.get_tasks_by_tags(tags)

    def get_tasks_by_assignee(self, user: User) -> list[Task]:
        return self.task_repository.get_tasks_by_assignee(user)

    def get_tasks_by_creator(self, user: User) -> list[Task]:
        return self.task_repository.get_tasks_by_creator(user)

    def get_all_tasks(self) -> list[Task]:
        return self.task_repository.get_all_tasks()

    def update_task_title(self, task_id: str, title: str) -> None:
        task = self._get_task_by_id_or_raise(task_id)
        task.update_title(title)
        self.task_repository.update_task(task)

    def update_task_description(self, task_id: str, description: str) -> None:
        task = self._get_task_by_id_or_raise(task_id)
        task.update_description(description)
        self.task_repository.update_task(task)

    def update_task_due_date(self, task_id: str, due_date: datetime) -> None:
        task = self._get_task_by_id_or_raise(task_id)
        task.update_due_date(due_date)
        self.task_repository.update_task(task)

    def update_task_priority(self, task_id: str, priority: TaskPriority) -> None:
        task = self._get_task_by_id_or_raise(task_id)
        task.update_priority(priority)
        self.task_repository.update_task(task)

    def add_task_assignees(self, task_id: str, assignees: list[User]) -> None:
        task = self._get_task_by_id_or_raise(task_id)
        for user in assignees:
            if not self.user_repository.get_user_by_id(user.get_id()):
                raise ValueError(f"User {user.get_id()} not found in repository")
        task.add_assignees(assignees)
        self.task_repository.update_task(task)

    def remove_task_assignees(self, task_id: str, assignees: list[User]) -> None:
        task = self._get_task_by_id_or_raise(task_id)
        task.remove_assignees(assignees)
        self.task_repository.update_task(task)

    def add_task_tags(self, task_id: str, tags: list[TaskTag]) -> None:
        task = self._get_task_by_id_or_raise(task_id)
        task.add_tags(tags)
        self.task_repository.update_task(task)

    def remove_task_tags(self, task_id: str, tags: list[TaskTag]) -> None:
        task = self._get_task_by_id_or_raise(task_id)
        task.remove_tags(tags)
        self.task_repository.update_task(task)

    def add_task_comment(self, task_id: str, comment_text: str, author: User) -> None:
        task = self._get_task_by_id_or_raise(task_id)
        if not self.user_repository.get_user_by_id(author.get_id()):
            raise ValueError("Author user not found in repository")
        comment = TaskComment(task, comment_text, author)
        task.add_comment(comment)
        self.task_repository.update_task(task)

    def start_task_progress(self, task_id: str) -> None:
        task = self._get_task_by_id_or_raise(task_id)
        task.start_progress()
        self.task_repository.update_task(task)

    def submit_task_for_review(self, task_id: str) -> None:
        task = self._get_task_by_id_or_raise(task_id)
        task.submit_for_review()
        self.task_repository.update_task(task)

    def complete_task(self, task_id: str) -> None:
        task = self._get_task_by_id_or_raise(task_id)
        task.complete_task()
        self.task_repository.update_task(task)

    def reopen_task(self, task_id: str) -> bool:
        task = self._get_task_by_id_or_raise(task_id)
        result = task.reopen_task()
        self.task_repository.update_task(task)
        return result

    def delete_task(self, task_id: str) -> None:
        task = self._get_task_by_id_or_raise(task_id)
        self.task_repository.remove_task(task)

    def create_task_list(self, name: str, created_by: User, tasks: Optional[list[Task]] = None) -> TaskList:
        if not self.user_repository.get_user_by_id(created_by.get_id()):
            raise ValueError("Creator user not found in repository")
        task_list = TaskList(name, created_by, tasks)
        self.task_repository.add_task_list(task_list)
        return task_list

    def get_task_list_by_id(self, task_list_id: str) -> Optional[TaskList]:
        return self.task_repository.get_task_list_by_id(task_list_id)

    def get_task_list_by_name(self, name: str) -> Optional[TaskList]:
        return self.task_repository.get_task_list_by_name(name)

    def get_task_lists_by_creator(self, user: User) -> list[TaskList]:
        return self.task_repository.get_task_lists_by_creator(user)

    def get_all_task_lists(self) -> list[TaskList]:
        return self.task_repository.get_all_task_lists()

    def add_task_to_list(self, task_list_id: str, task_id: str) -> None:
        task_list = self._get_task_list_by_id_or_raise(task_list_id)
        task = self._get_task_by_id_or_raise(task_id)
        task_list.add_sub_task(task)
        self.task_repository.update_task_list(task_list)

    def remove_task_from_list(self, task_list_id: str, task_id: str) -> None:
        task_list = self._get_task_list_by_id_or_raise(task_list_id)
        task = self._get_task_by_id_or_raise(task_id)
        task_list.remove_sub_task(task)
        self.task_repository.update_task_list(task_list)

    def update_task_list_status(self, task_list_id: str, status: TaskStatus) -> None:
        task_list = self._get_task_list_by_id_or_raise(task_list_id)
        task_list.set_status(status)
        self.task_repository.update_task_list(task_list)

    def delete_task_list(self, task_list_id: str) -> None:
        task_list = self._get_task_list_by_id_or_raise(task_list_id)
        self.task_repository.remove_task_list(task_list)

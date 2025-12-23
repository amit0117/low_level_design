# Task will have comments (for clarification and files attachments)
# But Comments will be either linear or at max 1 level deep
# Why 1 level deep?
# Because
# Deep nesting (comments of comments of comments) often leads to important updates getting "buried" in collapsed sub-threads, which is counterproductive for project accountability
# It's not like social media type comments where we can have infinite nesting.add()

# We will use a Builder pattern to create a Task object, because it's a complex object with many optional parameters


# Why to use Statuses and Tags?
# Statuses show where a task is.
# Tags explain what the task is, why it matters, and how to handle it.
# Tags are important because they enable cross-dimensional filtering and searching across tasks.
# if there is some task in Engineering dep, Sales Dep, Marketing Dep etc. And all of them have a common tags like 'URGENT', 'NEED_APPROVAL'
# So when we search for 'URGENT' or 'NEED_APPROVAL' tasks, we will get all the tasks from all the departments.


from typing import Optional, TYPE_CHECKING
from datetime import datetime
from app.models.task import Task
from app.models.enums import TaskStatus, TaskPriority, TaskTag
from app.states.task import TaskState

if TYPE_CHECKING:
    from app.models.user import User


class TaskBuilder:
    def __init__(self):
        self._title: Optional[str] = None
        self._created_by: Optional["User"] = None
        self._description: Optional[str] = None
        self._due_date: Optional[datetime] = None
        self._priority: Optional[TaskPriority] = None
        self._status: Optional[TaskStatus] = None
        self._assigned_users: Optional[list["User"]] = None
        self._tags: Optional[list[TaskTag]] = None
        self._parent_task_id: Optional[Task] = None
        self._state: Optional[TaskState] = None

    def set_title(self, title: str) -> "TaskBuilder":
        self._title = title
        return self

    def set_created_by(self, created_by: "User") -> "TaskBuilder":
        self._created_by = created_by
        return self

    def set_description(self, description: str) -> "TaskBuilder":
        self._description = description
        return self

    def set_due_date(self, due_date: datetime) -> "TaskBuilder":
        self._due_date = due_date
        return self

    def set_priority(self, priority: TaskPriority) -> "TaskBuilder":
        self._priority = priority
        return self

    def set_status(self, status: TaskStatus) -> "TaskBuilder":
        self._status = status
        return self

    def set_assigned_users(self, assigned_users: list["User"]) -> "TaskBuilder":
        self._assigned_users = assigned_users
        return self

    def set_tags(self, tags: list[TaskTag]) -> "TaskBuilder":
        self._tags = tags
        return self

    def set_parent_task_id(self, parent_task_id: Task) -> "TaskBuilder":
        self._parent_task_id = parent_task_id
        return self

    def set_state(self, state: TaskState) -> "TaskBuilder":
        self._state = state
        return self

    def build(self) -> Task:
        if not self._title:
            raise ValueError("Title is required to create a Task")
        if not self._created_by:
            raise ValueError("Created by user is required to create a Task")

        return Task(
            title=self._title,
            created_by=self._created_by,
            description=self._description,
            due_date=self._due_date,
            priority=self._priority,
            status=self._status,
            assigned_users=self._assigned_users,
            tags=self._tags,
            parent_task_id=self._parent_task_id,
            state=self._state,
        )

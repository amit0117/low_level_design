from typing import Optional, TYPE_CHECKING
from datetime import datetime
from app.models.enums import TaskStatus, TaskTag, TaskPriority
from uuid import uuid4
from app.states.task import TaskState
from app.observers.task import TaskSubject
from threading import Lock
from app.states.task import TodoState
from app.models.activity_log import ActivityLog

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.task_comment import TaskComment


class Task(TaskSubject):
    def __init__(
        self,
        title: str,
        created_by: "User",
        description: Optional[str] = None,
        due_date: Optional[datetime] = None,
        priority: Optional[TaskPriority] = None,
        status: Optional[TaskStatus] = None,
        assigned_users: Optional[list["User"]] = None,
        tags: Optional[list[TaskTag]] = None,
        parent_task_id: Optional["Task"] = None,
        state: Optional[TaskState] = None,
    ):
        super().__init__()  # Initialize the TaskSubject
        self.lock = Lock()  # To ensure date integrity while updating task details
        self.id = str(uuid4())
        self.title = title
        self.created_by = created_by
        self.description: Optional[str] = description
        self.due_date: Optional[datetime] = due_date
        self.priority: Optional[TaskPriority] = priority
        self.assignees: Optional[list["User"]] = assigned_users
        self.created_at = datetime.now()
        self.tags: Optional[list[TaskTag]] = tags
        self.parent_task_id: Optional["Task"] = parent_task_id
        # Keep default state as TODO state
        self.current_state: Optional[TaskState] = TodoState()
        self.status: Optional[TaskStatus] = status or TaskStatus.TODO
        self.comments: Optional[list["TaskComment"]] = []  # Will keep the comments as append only
        self.activity_log: Optional[list["ActivityLog"]] = []  # Will keep the activity log as append only
        # Add the initial activity log for the task creation by the creator
        self.activity_log.append(ActivityLog(self, created_by, "Task created"))
        # Add the assignees as observers
        if assigned_users:
            for assignee in assigned_users:
                self.add_observer(assignee)
                assignee.add_task_to_history(self)
        # Add the creator as an observer
        self.add_observer(created_by)

    def __del__(self) -> None:
        # Before deleting the task, we need to remove the task from all the observers
        if self.assignees:
            for observer in self.assignees:
                observer.remove_task_from_history(self)
        # Remove the creator as an observer
        self.remove_observer(self.created_by)

    def get_id(self) -> str:
        return self.id

    def get_title(self) -> str:
        return self.title

    def get_created_by(self) -> "User":
        return self.created_by

    def get_description(self) -> Optional[str]:
        return self.description

    def get_due_date(self) -> Optional[datetime]:
        return self.due_date

    def get_priority(self) -> Optional[TaskPriority]:
        return self.priority

    def get_status(self) -> Optional[TaskStatus]:
        return self.status

    def get_assignees(self) -> Optional[list["User"]]:
        return self.assignees

    def get_created_at(self) -> datetime:
        return self.created_at

    def get_tags(self) -> Optional[list[TaskTag]]:
        return self.tags

    def get_parent_task_id(self) -> Optional["Task"]:
        return self.parent_task_id

    def get_current_state(self) -> Optional[TaskState]:
        return self.current_state

    def get_comments(self) -> Optional[list["TaskComment"]]:
        return self.comments

    def get_activity_log(self) -> Optional[list["ActivityLog"]]:
        return self.activity_log

    def set_status(self, status: TaskStatus) -> None:
        with self.lock:
            self.status = status
            activity = ActivityLog(self, self.created_by, f"Task {self.title} status updated to {status}")
        self.notify_observers_on_task_status_change(self)
        self._add_activity_log_unsafe(activity)

    def set_state(self, state: TaskState) -> None:
        with self.lock:
            self.current_state = state
            self.notify_observers_on_task_status_change(self)

    def add_comment(self, comment: "TaskComment") -> None:
        with self.lock:
            self.comments.append(comment)
            self.notify_observers_on_task_comment_added(self, comment)

    def _add_activity_log_unsafe(self, activity: "ActivityLog") -> None:
        self.activity_log.append(activity)
        self.notify_observers_on_task_activity_log_added(self, activity)

    def add_activity_log(self, activity: "ActivityLog") -> None:
        with self.lock:
            self._add_activity_log_unsafe(activity)

    def update_title(self, title: str) -> None:
        with self.lock:
            self.title = title

    def set_parent_task_id(self, parent_task_id: "Task") -> None:
        with self.lock:
            self.parent_task_id = parent_task_id

    def update_description(self, description: str) -> None:
        with self.lock:
            self.description = description

    def update_due_date(self, due_date: datetime) -> None:
        with self.lock:
            self.due_date = due_date
            activity = ActivityLog(self, self.created_by, f"Task {self.title} due date updated to {due_date}")
        self._add_activity_log_unsafe(activity)

    def update_priority(self, priority: TaskPriority) -> None:
        with self.lock:
            self.priority = priority
            activity = ActivityLog(self, self.created_by, f"Task {self.title} priority updated to {priority}")
        self._add_activity_log_unsafe(activity)

    def add_assignees(self, assignees: list["User"]) -> None:
        with self.lock:
            for assignee in assignees:
                self.add_observer(assignee)
                assignee.add_task_to_history(self)

    def remove_assignees(self, assignees: list["User"]) -> None:
        with self.lock:
            for assignee in assignees:
                self.remove_observer(assignee)
                assignee.remove_task_from_history(self)

    def add_tags(self, tags: list[TaskTag]) -> None:
        with self.lock:
            for tag in tags:
                self.tags.append(tag)

    def remove_tags(self, tags: list[TaskTag]) -> None:
        with self.lock:
            for tag in tags:
                self.tags.remove(tag)

    def start_progress(self) -> None:
        self.current_state.start_progress(self)

    def submit_for_review(self) -> None:
        self.current_state.submit_for_review(self)

    def complete_task(self) -> None:
        self.current_state.complete_task(self)

    def reopen_task(self) -> bool:
        return self.current_state.reopen_task(self)

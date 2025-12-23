# 🚀 Task Management System - Low Level Design Implementation

A comprehensive implementation of a production-ready Task Management System demonstrating advanced design patterns, clean architecture, and enterprise-level features.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Design Patterns](#design-patterns)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This project implements a complete task management system featuring:

- **User Management**: Create and manage user accounts with task history tracking
- **Task Management**: Create, update, assign, and track tasks with multiple attributes
- **Task Lists**: Group tasks into lists (projects, sprints, etc.)
- **State Management**: State pattern for task lifecycle (TODO → IN_PROGRESS → IN_REVIEW → COMPLETED)
- **Search Functionality**: Multiple search strategies (Priority, Due Date, Assignee, Tags, Status)
- **Observer Pattern**: Real-time notifications for task updates, comments, and activity logs
- **Thread Safety**: Concurrent operations with proper locking mechanisms
- **Activity Logging**: Complete audit trail of all task activities

## ✨ Features

### Core Features

- ✅ **User Account Creation & Management**
- ✅ **Task Creation with Builder Pattern** (flexible task construction)
- ✅ **Task Assignment** (single or multiple assignees)
- ✅ **Task Status Management** (TODO, IN_PROGRESS, IN_REVIEW, COMPLETED)
- ✅ **Task Priority Levels** (LOW, MEDIUM, HIGH, URGENT)
- ✅ **Task Tagging System** (CRITICAL, URGENT, BUG, FEATURE, DEEP_WORK, etc.)
- ✅ **Task Comments** (linear comments for clarification)
- ✅ **Task Lists/Projects** (group related tasks together)
- ✅ **Due Date Management** (track and filter by due dates)
- ✅ **Activity Logging** (complete audit trail)
- ✅ **Task History** (per-user task tracking)

### Advanced Features

- 🔍 **Multiple Search Strategies** - Search by Priority, Due Date, Assignee, Tags, or Status
- 🎯 **State Pattern** - Enforced task state transitions with validation
- 🔔 **Observer Pattern** - Real-time notifications for status changes, comments, and activities
- 🏗️ **Repository Pattern** - Clean data access layer with thread safety
- 🔒 **Thread Safety** - Concurrent operations with proper locking mechanisms
- 📊 **Task Lists** - Group tasks into projects, sprints, or custom lists
- 🏷️ **Rich Tagging System** - Multi-dimensional task categorization
- 📝 **Activity Logs** - Complete history of all task modifications

## 🎨 Design Patterns

### 1. Singleton Pattern

Used for `TaskManager`, `TaskRepository`, and `UserRepository` to ensure single instance across the application.

```python
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

    @classmethod
    def get_instance(cls) -> "TaskManager":
        return cls._instance or cls()
```

### 2. Builder Pattern

Used for constructing complex `Task` objects with many optional parameters.

```python
task = (
    TaskBuilder()
    .set_title("Implement User Authentication")
    .set_created_by(rajesh)
    .set_description("Add login and signup functionality")
    .set_due_date(datetime.now() + timedelta(days=7))
    .set_priority(TaskPriority.HIGH)
    .set_assigned_users([priya])
    .set_tags([TaskTag.FEATURE, TaskTag.URGENT])
    .build()
)
```

### 3. Strategy Pattern

Used for implementing different search strategies.

```python
# Search by Priority
manager.add_task_search_strategy(TaskSearchByPriorityStrategy())
high_priority_tasks = manager.search_tasks(TaskPriority.HIGH)

# Search by Due Date
manager.add_task_search_strategy(TaskSearchByDueDateStrategy())
upcoming_tasks = manager.search_tasks(datetime.now() + timedelta(days=5))

# Search by Assignee
manager.add_task_search_strategy(TaskSearchByAssigneeStrategy())
user_tasks = manager.search_tasks(user)

# Search by Tags
manager.add_task_search_strategy(TaskSearchByTagsStrategy())
bug_tasks = manager.search_tasks([TaskTag.BUG])

# Search by Status
manager.add_task_search_strategy(TaskSearchByStatusStrategy())
todo_tasks = manager.search_tasks(TaskStatus.TODO)
```

### 4. State Pattern

Manages task lifecycle with enforced state transitions.

```python
# Task State Flow: TODO → IN_PROGRESS → IN_REVIEW → COMPLETED

# Start progress (TODO → IN_PROGRESS)
manager.start_task_progress(task_id)

# Submit for review (IN_PROGRESS → IN_REVIEW)
manager.submit_task_for_review(task_id)

# Complete task (IN_REVIEW → COMPLETED)
manager.complete_task(task_id)

# Reopen task (COMPLETED → TODO)
manager.reopen_task(task_id)
```

**State Transitions:**
- `TodoState`: Initial state, can only transition to `InProgressState`
- `InProgressState`: Can transition to `InReviewState`
- `InReviewState`: Can transition to `CompletedState`
- `CompletedState`: Can be reopened to `TodoState`

### 5. Observer Pattern

Real-time notifications for task updates.

```python
class User(TaskObserver):
    def update_on_task_status_change(self, task: Task) -> None:
        print(f"Task {task.get_title()} status changed to {task.get_status()}")

    def update_on_task_comment_added(self, task: Task, comment: TaskComment) -> None:
        print(f"New comment on task {task.get_title()}: {comment.get_text()}")

    def update_on_task_activity_log_added(self, task: Task, activity: ActivityLog) -> None:
        print(f"Activity on task {task.get_title()}: {activity.get_message()}")
```

### 6. Repository Pattern

Clean data access layer with thread-safe operations.

```python
class TaskRepository:
    def add_task(self, task: Task) -> None:
        with self.process_lock:
            self.tasks[task.get_id()] = task

    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        return self.tasks.get(task_id)

    def get_tasks_by_status(self, status: TaskStatus) -> list[Task]:
        return [task for task in self.tasks.values() if task.get_status() == status]
```

## 🏗️ Architecture

### Clean Architecture Layers

```
┌─────────────────────────────────────────┐
│              Demo Layer                 │
│              (demo.py)                  │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│            Manager Layer                │
│         TaskManager (Facade)            │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│          Repository Layer               │
│    TaskRepository, UserRepository       │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│            Domain Layer                 │
│    Task, User, TaskList, TaskComment    │
│    ActivityLog, TaskTag                 │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│         Strategy/State Layer            │
│    TaskSearchStrategy implementations   │
│    TaskState implementations            │
│    Observer implementations             │
└─────────────────────────────────────────┘
```

### Key Components

- **Models**: Core business entities (Task, User, TaskList, TaskComment, ActivityLog)
- **Repositories**: Data access layer with thread safety
- **Strategies**: Search algorithm implementations
- **States**: Task lifecycle management
- **Observers**: Event handling and notifications
- **Builders**: Complex object construction

## 📁 Project Structure

```
taskManagementSystem/
├── app/
│   ├── models/
│   │   ├── task.py              # Task entity with state and observer capabilities
│   │   ├── user.py              # User entity with observer implementation
│   │   ├── task_list.py         # TaskList for grouping tasks
│   │   ├── task_comment.py      # TaskComment entity
│   │   ├── activity_log.py      # ActivityLog for audit trail
│   │   ├── tag.py               # Tag entity
│   │   └── enums.py             # TaskStatus, TaskPriority, TaskTag enums
│   ├── repositories/
│   │   ├── tasks.py             # TaskRepository with thread safety
│   │   └── users.py             # UserRepository
│   ├── services/
│   │   └── (Future service layer)
│   ├── strategies/
│   │   └── task_serarch.py      # Task search strategies
│   ├── states/
│   │   └── task.py              # Task state implementations
│   ├── observers/
│   │   └── task.py              # TaskObserver and TaskSubject
│   └── builders/
│       └── task.py              # TaskBuilder for flexible construction
├── task_manager.py              # Main TaskManager facade
├── demo.py                      # Comprehensive demo script
└── README.md                    # This file
```

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Setup Instructions

1. **Navigate to the project directory**

```bash
cd low_level_design/taskManagementSystem
```

2. **Create virtual environment (optional but recommended)**

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Run the demo**

```bash
python3 demo.py
```

## 💻 Usage

### Basic Usage

```python
from task_manager import TaskManager
from app.builders.task import TaskBuilder
from app.models.enums import TaskStatus, TaskPriority, TaskTag
from datetime import datetime, timedelta

# Get manager instance (Singleton)
manager = TaskManager.get_instance()

# Create users
rajesh = manager.create_user("Rajesh Kumar", "rajesh@example.com")
priya = manager.create_user("Priya Sharma", "priya@example.com")

# Create task using Builder Pattern
task = (
    TaskBuilder()
    .set_title("Implement User Authentication")
    .set_created_by(rajesh)
    .set_description("Add login and signup functionality")
    .set_due_date(datetime.now() + timedelta(days=7))
    .set_priority(TaskPriority.HIGH)
    .set_assigned_users([priya])
    .set_tags([TaskTag.FEATURE, TaskTag.URGENT])
    .build()
)

# Add task to system
manager.add_task(task)

# Update task
manager.update_task_title(task.get_id(), "Implement OAuth Authentication")
manager.update_task_priority(task.get_id(), TaskPriority.URGENT)

# State transitions
manager.start_task_progress(task.get_id())        # TODO → IN_PROGRESS
manager.submit_task_for_review(task.get_id())    # IN_PROGRESS → IN_REVIEW
manager.complete_task(task.get_id())              # IN_REVIEW → COMPLETED
manager.reopen_task(task.get_id())                # COMPLETED → TODO

# Add comments
manager.add_task_comment(task.get_id(), "Started working on OAuth integration", priya)

# Create task list
task_list = manager.create_task_list("Sprint 1", rajesh, [task])
manager.add_task_to_list(task_list.get_id(), another_task.get_id())
```

### Advanced Usage

```python
# Search by Priority
manager.add_task_search_strategy(TaskSearchByPriorityStrategy())
high_priority_tasks = manager.search_tasks(TaskPriority.HIGH)

# Search by Due Date
manager.add_task_search_strategy(TaskSearchByDueDateStrategy())
upcoming_tasks = manager.search_tasks(datetime.now() + timedelta(days=5))

# Search by Assignee
manager.add_task_search_strategy(TaskSearchByAssigneeStrategy())
user_tasks = manager.search_tasks(priya)

# Search by Tags
manager.add_task_search_strategy(TaskSearchByTagsStrategy())
bug_tasks = manager.search_tasks([TaskTag.BUG, TaskTag.CRITICAL])

# Search by Status
manager.add_task_search_strategy(TaskSearchByStatusStrategy())
todo_tasks = manager.search_tasks(TaskStatus.TODO)

# Repository queries
tasks_by_creator = manager.get_tasks_by_creator(rajesh)
tasks_by_assignee = manager.get_tasks_by_assignee(priya)
tasks_by_priority = manager.get_tasks_by_priority(TaskPriority.URGENT)
tasks_by_status = manager.get_tasks_by_status(TaskStatus.IN_PROGRESS)

# Task history
user_task_history = rajesh.get_task_history()
```

## 📚 API Reference

### TaskManager (Facade)

```python
class TaskManager:
    @classmethod
    def get_instance(cls) -> "TaskManager"

    # User Management
    def create_user(self, name: str, email: str) -> User
    def get_user_by_id(self, user_id: str) -> Optional[User]
    def get_user_by_email(self, email: str) -> Optional[User]
    def get_all_users(self) -> list[User]
    def delete_user(self, user_id: str) -> None

    # Task Management
    def add_task(self, task: Task) -> None
    def get_task_by_id(self, task_id: str) -> Optional[Task]
    def get_all_tasks(self) -> list[Task]
    def delete_task(self, task_id: str) -> None

    # Task Updates
    def update_task_title(self, task_id: str, title: str) -> None
    def update_task_description(self, task_id: str, description: str) -> None
    def update_task_due_date(self, task_id: str, due_date: datetime) -> None
    def update_task_priority(self, task_id: str, priority: TaskPriority) -> None
    def add_task_assignees(self, task_id: str, assignees: list[User]) -> None
    def remove_task_assignees(self, task_id: str, assignees: list[User]) -> None
    def add_task_tags(self, task_id: str, tags: list[TaskTag]) -> None
    def remove_task_tags(self, task_id: str, tags: list[TaskTag]) -> None

    # Task State Management
    def start_task_progress(self, task_id: str) -> None
    def submit_task_for_review(self, task_id: str) -> None
    def complete_task(self, task_id: str) -> None
    def reopen_task(self, task_id: str) -> bool

    # Task Comments
    def add_task_comment(self, task_id: str, comment_text: str, author: User) -> None

    # Task Lists
    def create_task_list(self, name: str, created_by: User, tasks: Optional[list[Task]]) -> TaskList
    def get_task_list_by_id(self, task_list_id: str) -> Optional[TaskList]
    def get_all_task_lists(self) -> list[TaskList]
    def add_task_to_list(self, task_list_id: str, task_id: str) -> None
    def remove_task_from_list(self, task_list_id: str, task_id: str) -> None
    def update_task_list_status(self, task_list_id: str, status: TaskStatus) -> None
    def delete_task_list(self, task_list_id: str) -> None

    # Search
    def add_task_search_strategy(self, strategy: TaskSearchStrategy) -> None
    def search_tasks(self, query: Any) -> list[Task]

    # Repository Queries
    def get_tasks_by_status(self, status: TaskStatus) -> list[Task]
    def get_tasks_by_priority(self, priority: TaskPriority) -> list[Task]
    def get_tasks_by_tags(self, tags: list[TaskTag]) -> list[Task]
    def get_tasks_by_assignee(self, user: User) -> list[Task]
    def get_tasks_by_creator(self, user: User) -> list[Task]
```

### Task Model

```python
class Task(TaskSubject):
    def __init__(self, title: str, created_by: User, ...)
    def get_id(self) -> str
    def get_title(self) -> str
    def get_status(self) -> Optional[TaskStatus]
    def get_priority(self) -> Optional[TaskPriority]
    def get_assignees(self) -> Optional[list[User]]
    def get_tags(self) -> Optional[list[TaskTag]]
    def get_comments(self) -> Optional[list[TaskComment]]
    def get_activity_log(self) -> Optional[list[ActivityLog]]
    def get_due_date(self) -> Optional[datetime]
```

### TaskBuilder

```python
class TaskBuilder:
    def set_title(self, title: str) -> "TaskBuilder"
    def set_created_by(self, created_by: User) -> "TaskBuilder"
    def set_description(self, description: str) -> "TaskBuilder"
    def set_due_date(self, due_date: datetime) -> "TaskBuilder"
    def set_priority(self, priority: TaskPriority) -> "TaskBuilder"
    def set_assigned_users(self, assigned_users: list[User]) -> "TaskBuilder"
    def set_tags(self, tags: list[TaskTag]) -> "TaskBuilder"
    def build(self) -> Task
```

### Search Strategies

```python
class TaskSearchStrategy(ABC):
    @abstractmethod
    def search(self, query: Any) -> list[Task]

class TaskSearchByPriorityStrategy(TaskSearchStrategy)
class TaskSearchByDueDateStrategy(TaskSearchStrategy)
class TaskSearchByAssigneeStrategy(TaskSearchStrategy)
class TaskSearchByTagsStrategy(TaskSearchStrategy)
class TaskSearchByStatusStrategy(TaskSearchStrategy)
```

### Task States

```python
class TaskState(ABC):
    @abstractmethod
    def start_progress(self, task: Task) -> None
    @abstractmethod
    def submit_for_review(self, task: Task) -> None
    @abstractmethod
    def complete_task(self, task: Task) -> None
    @abstractmethod
    def reopen_task(self, task: Task) -> bool

class TodoState(TaskState)
class InProgressState(TaskState)
class InReviewState(TaskState)
class CompletedState(TaskState)
```

## 🎯 Examples

### Example 1: Create and Manage Tasks

```python
from task_manager import TaskManager
from app.builders.task import TaskBuilder
from app.models.enums import TaskPriority, TaskTag
from datetime import datetime, timedelta

manager = TaskManager.get_instance()

# Create users
rajesh = manager.create_user("Rajesh Kumar", "rajesh@example.com")
priya = manager.create_user("Priya Sharma", "priya@example.com")

# Create task
task = (
    TaskBuilder()
    .set_title("Fix Payment Gateway Bug")
    .set_created_by(rajesh)
    .set_description("Payment is failing for credit cards")
    .set_due_date(datetime.now() + timedelta(days=3))
    .set_priority(TaskPriority.URGENT)
    .set_assigned_users([priya])
    .set_tags([TaskTag.BUG, TaskTag.CRITICAL])
    .build()
)

manager.add_task(task)

# Update task
manager.update_task_priority(task.get_id(), TaskPriority.HIGH)
manager.add_task_comment(task.get_id(), "Started investigating", priya)

# State transitions
manager.start_task_progress(task.get_id())
manager.submit_task_for_review(task.get_id())
manager.complete_task(task.get_id())
```

### Example 2: Task Lists (Projects/Sprints)

```python
# Create task list
task_list = manager.create_task_list("Sprint 1", rajesh, [task1, task2])

# Add more tasks to list
manager.add_task_to_list(task_list.get_id(), task3.get_id())

# Update list status
manager.update_task_list_status(task_list.get_id(), TaskStatus.IN_PROGRESS)

# Get all tasks in list
tasks_in_list = task_list.get_sub_tasks()
```

### Example 3: Search Functionality

```python
# Search by priority
manager.add_task_search_strategy(TaskSearchByPriorityStrategy())
urgent_tasks = manager.search_tasks(TaskPriority.URGENT)

# Search by due date
manager.add_task_search_strategy(TaskSearchByDueDateStrategy())
upcoming = manager.search_tasks(datetime.now() + timedelta(days=7))

# Search by assignee
manager.add_task_search_strategy(TaskSearchByAssigneeStrategy())
my_tasks = manager.search_tasks(priya)

# Search by tags
manager.add_task_search_strategy(TaskSearchByTagsStrategy())
bug_tasks = manager.search_tasks([TaskTag.BUG, TaskTag.CRITICAL])
```

### Example 4: Observer Pattern

```python
# Users automatically become observers when assigned to tasks
# They receive notifications for:
# - Task status changes
# - New comments
# - Activity log updates

# When task status changes
manager.start_task_progress(task_id)
# All observers (assignees and creator) are notified

# When comment is added
manager.add_task_comment(task_id, "Please review", rajesh)
# All observers receive notification
```

## 🧪 Testing

### Running the Demo

```bash
# Run the comprehensive demo
python3 demo.py
```

The demo covers:
- User creation and management
- Task creation with Builder Pattern
- Task updates and modifications
- Task assignment and tagging
- State transitions
- Comments and activity logs
- Task lists
- Search strategies
- Observer notifications
- Repository queries
- Task and list deletion

### Test Structure

The demo script (`demo.py`) includes comprehensive examples of:
- ✅ All CRUD operations
- ✅ State pattern transitions
- ✅ Search strategies
- ✅ Observer notifications
- ✅ Task list management
- ✅ Thread-safe operations

## 🔧 Configuration

### Thread Safety

All operations are thread-safe using locks:
- `TaskManager` uses singleton pattern with thread-safe initialization
- `TaskRepository` and `UserRepository` use locks for concurrent access
- `Task` and `TaskList` use locks for state modifications

### Customization

```python
# Custom search strategy
class TaskSearchByCustomStrategy(TaskSearchStrategy):
    def search(self, query: Any) -> list[Task]:
        # Your custom search logic
        return filtered_tasks

# Custom observer
class CustomTaskObserver(TaskObserver):
    def update_on_task_status_change(self, task: Task) -> None:
        # Your custom notification logic
        pass
```

## 🚀 Performance

### Optimizations

- **Thread Safety**: All operations use locks for concurrent safety
- **Singleton Pattern**: Reduces memory footprint
- **Lazy Loading**: Repositories load data on-demand
- **Efficient Search**: Strategy pattern allows optimized search implementations

### Design Considerations

- **Builder Pattern**: Simplifies complex task construction
- **State Pattern**: Enforces valid state transitions
- **Repository Pattern**: Clean separation of data access
- **Observer Pattern**: Decoupled notification system
- **Strategy Pattern**: Flexible search implementations

## 🤝 Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests for new functionality
5. Run the demo: `python3 demo.py`
6. Commit changes: `git commit -m "Add feature"`
7. Push to branch: `git push origin feature-name`
8. Create a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Use type hints for all function parameters and return values
- Add docstrings for all public methods
- Follow SOLID principles
- Use design patterns appropriately

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../../LICENSE) file for details.

## 🙏 Acknowledgments

- Design patterns from Gang of Four
- Clean Architecture principles by Robert C. Martin
- SOLID principles
- Python best practices and conventions

## 📞 Support

For questions, issues, or contributions:

- Create an issue on GitHub
- Review the demo script for usage examples
- Check the code comments for implementation details

---

## 🎓 Key Learning Points

### Design Patterns Demonstrated

1. **Singleton**: Single instance of managers and repositories
2. **Builder**: Flexible task construction
3. **Strategy**: Multiple search algorithms
4. **State**: Task lifecycle management
5. **Observer**: Event-driven notifications
6. **Repository**: Data access abstraction

### SOLID Principles

- **Single Responsibility**: Each class has one reason to change
- **Open/Closed**: Open for extension (strategies, states), closed for modification
- **Liskov Substitution**: All state implementations are interchangeable
- **Interface Segregation**: Focused interfaces (TaskObserver, TaskState)
- **Dependency Inversion**: Depend on abstractions (strategies, states)

### Best Practices

- ✅ Thread-safe operations
- ✅ Type hints throughout
- ✅ Clean separation of concerns
- ✅ Comprehensive error handling
- ✅ Activity logging for audit trail
- ✅ Observer pattern for decoupled notifications

---

**Made with ❤️ using Python, Design Patterns, and Clean Architecture principles**


from datetime import datetime, timedelta
from task_manager import TaskManager
from app.builders.task import TaskBuilder
from app.models.enums import TaskStatus, TaskPriority, TaskTag
from app.strategies.task_serarch import (
    TaskSearchByPriorityStrategy,
    TaskSearchByDueDateStrategy,
    TaskSearchByAssigneeStrategy,
    TaskSearchByTagsStrategy,
    TaskSearchByStatusStrategy,
)


def main():
    manager = TaskManager.get_instance()

    print("=== Task Management System Demo ===\n")

    print("1. Creating Users")
    rajesh = manager.create_user("Rajesh Kumar", "rajesh@example.com")
    priya = manager.create_user("Priya Sharma", "priya@example.com")
    amit = manager.create_user("Amit Patel", "amit@example.com")
    print(f"Created users: {rajesh.get_name()}, {priya.get_name()}, {amit.get_name()}\n")

    print("2. Creating Tasks using Builder Pattern")
    task1 = (
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
    manager.add_task(task1)

    task2 = (
        TaskBuilder()
        .set_title("Fix Payment Gateway Bug")
        .set_created_by(priya)
        .set_description("Payment is failing for credit cards")
        .set_due_date(datetime.now() + timedelta(days=3))
        .set_priority(TaskPriority.URGENT)
        .set_assigned_users([amit])
        .set_tags([TaskTag.BUG, TaskTag.CRITICAL])
        .build()
    )
    manager.add_task(task2)

    task3 = (
        TaskBuilder()
        .set_title("Design Database Schema")
        .set_created_by(amit)
        .set_description("Design schema for user management")
        .set_due_date(datetime.now() + timedelta(days=14))
        .set_priority(TaskPriority.MEDIUM)
        .set_tags([TaskTag.DEEP_WORK])
        .build()
    )
    manager.add_task(task3)

    print(f"Created {len(manager.get_all_tasks())} tasks\n")

    print("3. Testing Task Updates")
    manager.update_task_title(task1.get_id(), "Implement User Authentication with OAuth")
    manager.update_task_description(task1.get_id(), "Add login, signup, and OAuth integration")
    manager.update_task_priority(task2.get_id(), TaskPriority.HIGH)
    manager.update_task_due_date(task3.get_id(), datetime.now() + timedelta(days=10))
    print("Task updates completed\n")

    print("4. Testing Task Assignment")
    manager.add_task_assignees(task3.get_id(), [rajesh, priya])
    print("Task assignment completed\n")

    print("5. Testing Task State Transitions")
    print(f"Task1 initial status: {task1.get_status()}")
    manager.start_task_progress(task1.get_id())
    print(f"Task1 after start_progress: {task1.get_status()}")
    manager.submit_task_for_review(task1.get_id())
    print(f"Task1 after submit_for_review: {task1.get_status()}")
    manager.complete_task(task1.get_id())
    print(f"Task1 after complete: {task1.get_status()}")
    manager.reopen_task(task1.get_id())
    print(f"Task1 after reopen: {task1.get_status()}\n")

    print("6. Testing Task Comments")
    manager.add_task_comment(task2.get_id(), "Started investigating the issue", amit)
    manager.add_task_comment(task2.get_id(), "Found the root cause in payment processor", amit)
    print(f"Task2 has {len(task2.get_comments())} comments\n")

    print("7. Testing Task Tags")
    manager.add_task_tags(task3.get_id(), [TaskTag.INTERNAL, TaskTag.DEEP_WORK])
    print(f"Task3 tags: {[tag.value for tag in task3.get_tags()]}\n")

    print("8. Testing Search Strategies")
    print("8.1 Search by Priority (HIGH)")
    manager.add_task_search_strategy(TaskSearchByPriorityStrategy())
    high_priority_tasks = manager.search_tasks(TaskPriority.HIGH)
    print(f"Found {len(high_priority_tasks)} high priority tasks")

    print("8.2 Search by Due Date")
    manager.add_task_search_strategy(TaskSearchByDueDateStrategy())
    upcoming_tasks = manager.search_tasks(datetime.now() + timedelta(days=5))
    print(f"Found {len(upcoming_tasks)} tasks due within 5 days")

    print("8.3 Search by Assignee")
    manager.add_task_search_strategy(TaskSearchByAssigneeStrategy())
    amit_tasks = manager.search_tasks(amit)
    print(f"Found {len(amit_tasks)} tasks assigned to {amit.get_name()}")

    print("8.4 Search by Tags")
    manager.add_task_search_strategy(TaskSearchByTagsStrategy())
    bug_tasks = manager.search_tasks([TaskTag.BUG])
    print(f"Found {len(bug_tasks)} tasks with BUG tag")

    print("8.5 Search by Status")
    manager.add_task_search_strategy(TaskSearchByStatusStrategy())
    todo_tasks = manager.search_tasks(TaskStatus.TODO)
    print(f"Found {len(todo_tasks)} tasks with TODO status\n")

    print("9. Testing Task Lists")
    task_list = manager.create_task_list("Sprint 1", rajesh, [task1, task2])
    print(f"Created task list: {task_list.get_name()} with {len(task_list.get_sub_tasks())} tasks")
    manager.add_task_to_list(task_list.get_id(), task3.get_id())
    print(f"Added task3 to list. List now has {len(task_list.get_sub_tasks())} tasks")
    manager.update_task_list_status(task_list.get_id(), TaskStatus.IN_PROGRESS)
    print(f"Task list status: {task_list.get_status()}\n")

    print("10. Testing Observer Pattern")
    print("Creating task4 and assigning to multiple users to test notifications:")
    task4 = (
        TaskBuilder()
        .set_title("Code Review for Authentication")
        .set_created_by(rajesh)
        .set_assigned_users([priya, amit])
        .set_priority(TaskPriority.MEDIUM)
        .build()
    )
    manager.add_task(task4)
    print(f"Task4 created and assigned to {len(task4.get_assignees())} users")
    print("Changing task4 status to trigger observer notifications:")
    manager.start_task_progress(task4.get_id())
    manager.add_task_comment(task4.get_id(), "Please review the authentication code", rajesh)
    print("Observer notifications should have been triggered\n")

    print("11. Testing Task History")
    print(f"{rajesh.get_name()} task history: {len(rajesh.get_task_history())} tasks")
    print(f"{priya.get_name()} task history: {len(priya.get_task_history())} tasks")
    print(f"{amit.get_name()} task history: {len(amit.get_task_history())} tasks\n")

    print("12. Testing Repository Queries")
    tasks_by_rajesh = manager.get_tasks_by_creator(rajesh)
    print(f"Tasks created by {rajesh.get_name()}: {len(tasks_by_rajesh)}")
    tasks_assigned_to_priya = manager.get_tasks_by_assignee(priya)
    print(f"Tasks assigned to {priya.get_name()}: {len(tasks_assigned_to_priya)}")
    urgent_tasks = manager.get_tasks_by_priority(TaskPriority.URGENT)
    print(f"Urgent priority tasks: {len(urgent_tasks)}\n")

    print("13. Testing Task Deletion")
    print(f"Total tasks before deletion: {len(manager.get_all_tasks())}")
    manager.delete_task(task4.get_id())
    print(f"Total tasks after deletion: {len(manager.get_all_tasks())}\n")

    print("14. Testing Task List Deletion")
    print(f"Total task lists before deletion: {len(manager.get_all_task_lists())}")
    manager.delete_task_list(task_list.get_id())
    print(f"Total task lists after deletion: {len(manager.get_all_task_lists())}\n")

    print("15. Final Summary")
    print(f"Total users: {len(manager.get_all_users())}")
    print(f"Total tasks: {len(manager.get_all_tasks())}")
    print(f"Total task lists (Must be 0 as we deleted the task list items): {len(manager.get_all_task_lists())}")
    print("\n=== Demo Completed ===")


if __name__ == "__main__":
    main()

"""Task Tracker CLI — a simple in-memory task manager.

NOTE FOR LEARNERS: This file has one intentional bug:
  - create_task uses unsanitized string formatting that breaks on
    special characters like curly braces in task titles.
"""

from config import get_config
from utils import format_user_name, truncate_string


tasks = []


def create_task(title, assignee_first=None, assignee_last=None):
    """Create a new task and add it to the in-memory list.

    BUG: Uses str.format() on user-supplied title. If the title contains
    curly braces (e.g., "Fix {config} loader"), it raises KeyError or
    IndexError. Should use f-string or %-formatting with the value directly.
    """
    config = get_config()

    if len(tasks) >= config["max_tasks"]:
        return None

    assignee = None
    if assignee_first and assignee_last:
        assignee = format_user_name(assignee_first, assignee_last)

    task = {
        "id": len(tasks) + 1,
        "title": "Task: {}".format(title),
        "assignee": assignee,
        "status": "open",
        "display_title": truncate_string(title),
    }
    tasks.append(task)
    return task


def list_tasks(status=None):
    """List all tasks, optionally filtered by status."""
    if status is None:
        return list(tasks)
    return [t for t in tasks if t["status"] == status]


def complete_task(task_id):
    """Mark a task as completed by ID."""
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "completed"
            return task
    return None


def get_summary():
    """Return a summary of task counts by status."""
    summary = {"total": len(tasks), "open": 0, "completed": 0}
    for task in tasks:
        if task["status"] in summary:
            summary[task["status"]] += 1
    return summary


if __name__ == "__main__":
    create_task("Set up project", "Jane", "Doe")
    create_task("Write tests", "John", "Smith")
    create_task("Deploy to staging")

    print(f"Tasks: {get_summary()}")
    for t in list_tasks():
        print(f"  [{t['status']}] {t['display_title']} — {t['assignee'] or 'Unassigned'}")

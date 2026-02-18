"""Tests for main.py.

All tests here pass — this file validates the basic happy-path behavior.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from main import create_task, list_tasks, complete_task, get_summary, tasks


def setup_function():
    """Clear the task list before each test."""
    tasks.clear()


def test_create_task_basic():
    task = create_task("Write documentation")
    assert task is not None
    assert task["id"] == 1
    assert task["status"] == "open"
    assert "Write documentation" in task["title"]


def test_create_task_with_assignee():
    task = create_task("Fix bug", "Jane", "Doe")
    assert task["assignee"] == "Jane Doe"


def test_create_task_without_assignee():
    task = create_task("Deploy app")
    assert task["assignee"] is None


def test_list_tasks_all():
    create_task("Task 1")
    create_task("Task 2")
    assert len(list_tasks()) == 2


def test_list_tasks_by_status():
    create_task("Task 1")
    create_task("Task 2")
    complete_task(1)
    assert len(list_tasks("open")) == 1
    assert len(list_tasks("completed")) == 1


def test_complete_task():
    create_task("Task 1")
    result = complete_task(1)
    assert result["status"] == "completed"


def test_complete_nonexistent_task():
    result = complete_task(999)
    assert result is None


def test_get_summary():
    create_task("Task 1")
    create_task("Task 2")
    complete_task(1)
    summary = get_summary()
    assert summary["total"] == 2
    assert summary["open"] == 1
    assert summary["completed"] == 1

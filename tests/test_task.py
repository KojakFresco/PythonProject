import pytest

from task_platform.exceptions import TaskPriorityError, TaskStatusError, TaskValidationError
from task_platform.task import Task


def test_task_with_correct_arguments():
    task = Task(id="task1", description="Test task", priority=3, status="pending")
    assert task.id == "task1"
    assert task.description == "Test task"
    assert task.priority == 3
    assert task.status == "pending"


def test_task_is_ready():
    task = Task(id="task3", description="Ready task", priority=4, status="pending")
    assert task.is_ready == True

    task.status = "completed"
    assert task.is_ready == False

    task.status = "in_progress"
    task.priority = 2
    assert task.is_ready == False


def test_task_from_data():
    from task_platform.task import TaskData

    task_data = TaskData(
        id="task4",
        payload={"description": "Task from data", "priority": 5, "status": "pending"},
    )
    task = Task.from_data(task_data)
    assert task.id == "task4"
    assert task.description == "Task from data"
    assert task.priority == 5
    assert task.status == "pending"


def test_task_exceptions():
    with pytest.raises(TaskValidationError):
        Task(id="task5", description="Invalid priority", priority=6, status="pending")

    with pytest.raises(TaskValidationError):
        Task(id="task6", description="Invalid status", priority=3, status="unknown")


def test_task_change_status():
    task = Task(id="task7", description="Status task", priority=3, status="pending")

    task.change_status("completed")
    assert task.status == "completed"

    with pytest.raises(TaskStatusError):
        task.change_status("broken")


def test_task_change_priority():
    task = Task(id="task8", description="Priority task", priority=3, status="pending")

    task.change_priority(5)
    assert task.priority == 5

    with pytest.raises(TaskPriorityError):
        task.change_priority(0)

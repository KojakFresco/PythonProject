from task_platform.task_queue import TaskQueue
from task_platform.task import Task, TaskData


def test_task_queue():
    task_queue = TaskQueue()
    task_queue.add_task(Task("1", "email", 1))
    task_queue.add_task(Task("2", "order", 2))

    for task in task_queue:
        assert task.id in ["1", "2"]


def test_task_queue_filters():
    task_queue = TaskQueue()
    task_queue.add_task(Task("1", "email", 1, status="pending"))
    task_queue.add_task(Task("2", "order", 2, status="completed"))

    pending_tasks = list(task_queue.filter_by_status("pending"))
    assert len(pending_tasks) == 1
    assert pending_tasks[0].id == "1"

    priority_2_tasks = list(task_queue.filter_by_priority(2))
    assert len(priority_2_tasks) == 1
    assert priority_2_tasks[0].id == "2"


def test_task_reuse():
    task_queue = TaskQueue()
    task_queue.add_task(Task("1", "email", 1))
    task_queue.add_task(Task("2", "order", 2))

    tasks = list(task_queue)
    assert len(tasks) == 2
    assert tasks[0].id == "1"
    assert tasks[1].id == "2"

    # Reuse the same queue to get tasks again
    tasks_again = list(task_queue)
    assert len(tasks_again) == 2
    assert tasks_again[0].id == "1"
    assert tasks_again[1].id == "2"


def test_task_queue_from_source():
    class MockTaskSource:
        def get_tasks(self):
            return [
                TaskData("3", payload={"description": "notification", "priority": 3})
            ]

    task_queue = TaskQueue()
    task_queue.from_source(MockTaskSource())

    tasks = list(task_queue)
    assert len(tasks) == 1
    assert tasks[0].id == "3"

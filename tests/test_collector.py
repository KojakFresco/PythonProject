import pytest

from task_platform.collector import collect_tasks
from task_platform.task import Task, TaskData


class FakeSource:
    def get_tasks(self):
        return [
            TaskData("1", {"description": "email"}),
            TaskData("2", {"description": "order"}),
        ]


class FakeSource2:
    def get_task(self):
        return [TaskData("1", {"type": "email"}), TaskData("2", {"type": "order"})]


def test_task_collector_with_correct_source():
    fake_tasks = [
        Task(id="1", description="email", priority=2),
        Task(id="2", description="order", priority=3),
    ]

    tasks = collect_tasks(FakeSource())

    assert list(tasks) == fake_tasks


def test_task_collector_with_incorrect_source():
    with pytest.raises(TypeError):
        list(collect_tasks(FakeSource2()))

import pytest

from task_platform.collector import collect_tasks
from task_platform.task import Task


class FakeSource:
    def get_tasks(self):
        return [Task("1", {"type": "email"}), Task("2", {"type": "order"})]

class FakeSource2:
    def get_task(self):
        return [Task("1", {"type": "email"}), Task("2", {"type": "order"})]

def test_task_collector_with_correct_source():
    fake_tasks = [
        Task("1", {"type": "email"}),
        Task("2", {"type": "order"}),
    ]

    tasks = collect_tasks(FakeSource())

    assert tasks == fake_tasks

def test_task_collector_with_incorrect_source():
    with pytest.raises(TypeError):
        collect_tasks(FakeSource2())
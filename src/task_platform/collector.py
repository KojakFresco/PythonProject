from typing import Iterable

from task_platform.protocols import TaskSource
from task_platform.task import Task


def collect_tasks(source: TaskSource) -> Iterable[Task]:

    if not isinstance(source, TaskSource):
        raise TypeError("Object does not implement TaskSource")

    return _collect_tasks_impl(source)


def _collect_tasks_impl(source: TaskSource) -> Iterable[Task]:
    for task_data in source.get_tasks():
        yield Task.from_data(task_data)

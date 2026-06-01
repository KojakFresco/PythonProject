from typing import Iterator

from task_platform.protocols import TaskSource
from task_platform.task import Task
from task_platform.collector import collect_tasks


class TaskQueue:
    def __init__(self) -> None:
        self._tasks = []
        self._generators = []

    def __iter__(self) -> Iterator[Task]:
        return self._get_tasks()

    def _get_tasks(self) -> Iterator[Task]:
        for task in self._tasks:
            yield task
        for generator in self._generators:
            for task in generator():
                yield task

    def add_task(self, task: Task) -> None:
        self._tasks.append(task)

    def from_source(self, source: TaskSource) -> None:
        self._generators.append(lambda s=source: collect_tasks(s))

    def filter_by_status(self, status: str) -> Iterator[Task]:
        for task in self:
            if task.status == status:
                yield task

    def filter_by_priority(self, priority: int) -> Iterator[Task]:
        for task in self:
            if task.priority == priority:
                yield task

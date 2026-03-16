from typing import Protocol, runtime_checkable, Iterable
from task_platform.task import Task


@runtime_checkable
class TaskSource(Protocol):
    def get_tasks(self) -> Iterable[Task]: ...

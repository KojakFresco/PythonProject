from typing import Protocol, runtime_checkable, Iterable, Any
from task_platform.task import TaskData, Task


@runtime_checkable
class TaskSource(Protocol):
    def get_tasks(self) -> Iterable[TaskData]: ...


@runtime_checkable
class TaskHandler(Protocol):
    @property
    def name(self) -> str: ...
    async def can_handle(self, task: Task) -> bool: ...
    async def handle(self, task: Task) -> Any: ...

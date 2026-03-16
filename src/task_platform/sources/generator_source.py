from typing import Iterable
from task_platform.task import Task


class GeneratorTaskSource:
    def __init__(self, count: int) -> None:
        self.count = count

    def get_tasks(self) -> Iterable[Task]:
        for i in range(self.count):
            yield Task(id=f"generated-{i}", payload={"type": "generated", "index": i})

from typing import Iterable
from task_platform.task import TaskData


class GeneratorTaskSource:
    def __init__(self, count: int) -> None:
        self.count = count

    def get_tasks(self) -> Iterable[TaskData]:
        for i in range(self.count):
            yield TaskData(
                id=f"generated-{i}",
                payload={
                    "description": "generated_task",
                    "type": "order",
                    "order_id": i,
                    "priority": i * (i % 3) % 5 + 1,
                },
            )

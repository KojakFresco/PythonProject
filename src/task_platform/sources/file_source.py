import json

from typing import Iterable
from task_platform.task import TaskData


class FileTaskSource:
    def __init__(self, path: str) -> None:
        self.path = path

    def get_tasks(self) -> Iterable[TaskData]:
        with open(self.path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for item in data:
            yield TaskData(item["id"], item["payload"])

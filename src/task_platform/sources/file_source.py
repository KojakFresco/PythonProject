import json

from typing import Iterable
from task_platform.task import Task


class FileTaskSource:
    def __init__(self, path: str) -> None:
        self.path = path

    def get_tasks(self) -> Iterable[Task]:
        with open(self.path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for item in data:
            yield Task(item["id"], item["payload"])

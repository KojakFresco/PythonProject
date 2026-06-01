from typing import Iterable

import requests
from task_platform.task import TaskData


class ApiTaskSource:
    def __init__(self, api_url: str = "http://127.0.0.1:8000/tasks") -> None:
        self.api_url = api_url

    def get_tasks(self) -> Iterable[TaskData]:
        response = requests.get(self.api_url)
        data = response.json()

        for item in data:
            yield TaskData(item["id"], item["payload"])

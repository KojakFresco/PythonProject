import asyncio

from task_platform.task import Task


class SimpleHandler:
    def __init__(self, name):
        self.name = name

    async def can_handle(self, task: Task) -> bool:
        return self.name == task.payload.get("type")

    async def handle(self, task: Task):
        print(f"{self.name} handling task: {task.id}")
        await asyncio.sleep(0.1)
        return {"status": "ok"}

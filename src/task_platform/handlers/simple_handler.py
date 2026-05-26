import asyncio
import logging

from task_platform.task import Task

logger = logging.getLogger(__name__)


class SimpleHandler:
    @property
    def name(self) -> str:
        return "SimpleHandler"

    async def can_handle(self, task: Task) -> bool:
        return True

    async def handle(self, task: Task):
        logger.info(f"{self.name} handling task: {task.id}")
        await asyncio.sleep(0.1)
        return {"status": "ok"}

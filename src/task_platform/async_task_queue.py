import asyncio

from task_platform.task import Task


class AsyncTaskQueue:
    def __init__(self, maxsize: int = 0):
        self._queue = asyncio.Queue(maxsize=maxsize)

    async def put(self, task: Task) -> None:
        await self._queue.put(task)

    async def get(self) -> Task:
        return await self._queue.get()

    def task_done(self) -> None:
        self._queue.task_done()

    async def join(self) -> None:
        await self._queue.join()

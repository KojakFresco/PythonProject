import asyncio
import logging

from task_platform.handlers.order_handler import OrderHandler
from task_platform.handlers.simple_handler import SimpleHandler
from task_platform.setup_logging import setup_logging
from task_platform.sources.generator_source import GeneratorTaskSource
from task_platform.async_task_queue import AsyncTaskQueue
from task_platform.async_executor import AsyncExecutor
from task_platform.task_queue import TaskQueue


def main():

    async def run_example():
        task_queue = TaskQueue()
        task_queue.from_source(GeneratorTaskSource(6))
        async_queue = AsyncTaskQueue()
        async_executor = AsyncExecutor(
            async_queue, [OrderHandler(), SimpleHandler()], graceful_timeout=2.0
        )
        async with async_executor.run(worker_count=3):
            for task in task_queue:
                await async_queue.put(task)
            await async_queue.join()

    asyncio.run(run_example())


if __name__ == "__main__":
    setup_logging(level=logging.DEBUG)
    main()

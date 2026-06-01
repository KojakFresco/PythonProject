import asyncio

from task_platform.collector import collect_tasks
from task_platform.sources.generator_source import GeneratorTaskSource
from task_platform.async_task_queue import AsyncTaskQueue
from task_platform.async_executor import AsyncExecutor
from task_platform.handlers.simple_handler import SimpleHandler


def test_collector_and_executor_integration():
    async def runner():
        src = GeneratorTaskSource(count=3)
        tasks = list(collect_tasks(src))

        queue = AsyncTaskQueue()
        handler = SimpleHandler()
        executor = AsyncExecutor(queue, [handler], graceful_timeout=0.5)

        async with executor.run(worker_count=2):
            for t in tasks:
                await queue.put(t)
            await asyncio.wait_for(queue.join(), timeout=2.0)

        assert executor.get_failed_tasks() == []

    asyncio.run(runner())

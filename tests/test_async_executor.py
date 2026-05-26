import asyncio
import pytest

from task_platform.async_task_queue import AsyncTaskQueue
from task_platform.async_executor import AsyncExecutor
from task_platform.task import Task


class TestHandlerSuccess:
    @property
    def name(self):
        return "success"

    async def can_handle(self, task: Task) -> bool:
        return True

    async def handle(self, task: Task):
        await asyncio.sleep(0)
        return {"status": "ok"}


class TestHandlerFail:
    @property
    def name(self):
        return "fail"

    async def can_handle(self, task: Task) -> bool:
        return True

    async def handle(self, task: Task):
        await asyncio.sleep(0)
        raise RuntimeError("handler failure")


class NeverHandle:
    @property
    def name(self):
        return "never"

    async def can_handle(self, task: Task) -> bool:
        return False

    async def handle(self, task: Task):
        return None


def test_executor_processes_task_success():
    async def runner():
        queue = AsyncTaskQueue()
        handler = TestHandlerSuccess()
        executor = AsyncExecutor(queue, [handler], graceful_timeout=0.5)

        task = Task(id="t1", description="desc", priority=3, payload={})

        async with executor.run(worker_count=1):
            await queue.put(task)
            await asyncio.wait_for(queue.join(), timeout=1.0)

        assert executor.get_failed_tasks() == []

    asyncio.run(runner())


@pytest.mark.asyncio
async def test_executor_records_failed_task_on_exception():
    queue = AsyncTaskQueue()
    handler = TestHandlerFail()
    executor = AsyncExecutor(queue, [handler], graceful_timeout=0.5)

    task = Task(id="t-fail", description="desc", priority=3, payload={})

    async with executor.run(worker_count=1):
        await queue.put(task)
        await asyncio.wait_for(queue.join(), timeout=1.0)

    failed = executor.get_failed_tasks()
    assert len(failed) == 1
    assert failed[0].id == task.id


@pytest.mark.asyncio
async def test_no_handler_records_failed():
    queue = AsyncTaskQueue()
    handler = NeverHandle()
    executor = AsyncExecutor(queue, [handler], graceful_timeout=0.5)

    task = Task(id="no-handler", description="desc", priority=3, payload={})

    async with executor.run(worker_count=1):
        await queue.put(task)
        await asyncio.wait_for(queue.join(), timeout=1.0)

    failed = executor.get_failed_tasks()
    assert len(failed) == 1
    assert failed[0].id == task.id


@pytest.mark.asyncio
async def test_worker_does_not_crash_on_empty_queue():
    queue = AsyncTaskQueue()
    executor = AsyncExecutor(queue, [])

    async with executor.run(worker_count=1):
        await asyncio.sleep(1.2)

        assert executor._running
        assert len(executor._workers) == 1
        assert not executor._workers[0].done()


@pytest.mark.asyncio
async def test_worker_cancelled_is_handled():
    queue = AsyncTaskQueue()
    executor = AsyncExecutor(queue, [], graceful_timeout=0.2)

    async with executor.run(worker_count=2):
        assert len(executor._workers) == 2
        assert all(not w.done() for w in executor._workers)

        cancelled_worker = executor._workers[0]
        cancelled_worker.cancel()

        await asyncio.sleep(0.1)

        assert cancelled_worker.done()
        assert cancelled_worker.cancelled()

        remaining_worker = executor._workers[1]
        assert not remaining_worker.done()

    assert not executor._running
    assert all(w.done() for w in executor._workers)

import asyncio
import logging
from contextlib import asynccontextmanager
from typing import List, Optional, AsyncGenerator

from task_platform.exceptions import NoHandlerError
from task_platform.task import Task
from task_platform.async_task_queue import AsyncTaskQueue
from task_platform.protocols import TaskHandler


logger = logging.getLogger(__name__)


class AsyncExecutor:
    """
    Асинхронный исполнитель задач.

    Управляет пулом воркеров, которые обрабатывают задачи из очереди
    с использованием подходящих обработчиков.
    """

    def __init__(
        self,
        queue: AsyncTaskQueue,
        handlers: List[TaskHandler],
        graceful_timeout: float = 5.0,
    ):
        """
        Инициализация исполнителя.

        Args:
            queue: Очередь задач
            handlers: Список обработчиков (проверяются в порядке добавления)
            graceful_timeout: Тайм-аут для остановки воркеров (секунды)
        """
        self._queue = queue
        self._handlers = handlers
        self._graceful_timeout = graceful_timeout

        self._workers: List[asyncio.Task] = []
        self._running = False
        self._worker_id_counter = 0
        self._failed_tasks: List[Task] = []

    @asynccontextmanager
    async def run(self, worker_count: int = 3) -> AsyncGenerator["AsyncExecutor", None]:
        """
        Контекстный менеджер для запуска и остановки исполнителя.

        Args:
            worker_count: Количество воркеров в пуле
        """
        self._running = True

        for i in range(worker_count):
            worker = asyncio.create_task(self._worker(i))
            self._workers.append(worker)
            logger.info(f"Worker {i} started")

        try:
            yield self
        finally:
            await self._stop()

    async def _stop(self) -> None:
        """Останавливает всех воркеров и освобождает ресурсы."""
        logger.info("Stopping executor...")
        self._running = False

        done, pending = await asyncio.wait(
            self._workers,
            timeout=self._graceful_timeout,
            return_when=asyncio.ALL_COMPLETED
        )

        for task in pending:
            task.cancel()

        if pending:
            await asyncio.gather(*pending, return_exceptions=True)
            logger.warning(f"Cancelled {len(pending)} worker(s)")

        logger.info("Executor stopped")

    async def _worker(self, worker_id: int) -> None:
        """
        Воркер — корутина, обрабатывающая задачи.

        Args:
            worker_id: Идентификатор воркера
        """
        logger.info(f"Worker {worker_id} started")

        while self._running:
            try:
                task = await asyncio.wait_for(
                    self._queue.get(),
                    timeout=1.0
                )
            except asyncio.TimeoutError:
                continue
            except asyncio.CancelledError:
                logger.info(f"Worker {worker_id} cancelled")
                return

            try:
                await self._process_task(worker_id, task)
            except Exception as e:
                logger.error(f"Worker {worker_id}: unexpected error: {e}", exc_info=True)
            finally:
                self._queue.task_done()

        logger.info(f"Worker {worker_id} stopped")

    async def _process_task(self, worker_id: int, task: Task) -> None:
        """
        Обрабатывает задачу: ищет обработчик и вызывает его.

        Args:
            worker_id: ID воркера
            task: Задача для обработки
        """
        try:
            logger.info(f"Worker {worker_id}: processing task {task.id}")

            handler = await self._find_handler(task)

            if handler is None:
                raise NoHandlerError(f"No handler found for task {task.id}")

            logger.debug(f"Worker {worker_id}: using {handler.name} for {task.id}")
            result = await handler.handle(task)

            logger.info(
                f"Worker {worker_id}: completed task {task.id} with result: {result}"
            )
        except NoHandlerError:
            logger.warning(f"Worker {worker_id}: no handler found for task {task.id}")
            self._failed_tasks.append(task)
        except Exception as e:
            logger.error(f"Worker {worker_id}: error processing task {task.id}: {e}", exc_info=True)
            self._failed_tasks.append(task)

    async def _find_handler(self, task: Task) -> Optional[TaskHandler]:
        """
        Находит подходящий обработчик для задачи.

        Args:
            task: Задача для проверки

        Returns:
            Обработчик или None, если не найден
        """
        for handler in self._handlers:
            if await handler.can_handle(task):
                return handler
        return None

    def get_failed_tasks(self) -> List[Task]:
        """Возвращает список задач, которые не удалось обработать."""
        return self._failed_tasks.copy()

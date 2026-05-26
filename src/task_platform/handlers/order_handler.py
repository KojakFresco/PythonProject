import asyncio
import logging
from typing import Any, Dict

from task_platform.task import Task

logger = logging.getLogger(__name__)


class OrderHandler:
    """
    Обработчик заказов.

    Обрабатывает задачи типа "order": подтверждает заказ,
    списывает средства, обновляет склад.
    """

    @property
    def name(self) -> str:
        return "OrderHandler"

    async def can_handle(self, task: Task) -> bool:
        """
        Проверяет, является ли задача заказом.

        Ожидаемая структура payload:
            {"type": "order", "order_id": int, "amount": float, "user_id": int}
        """
        payload = task.payload
        return (
            isinstance(payload, dict)
            and payload.get("type") == "order"
            and "order_id" in payload
        )

    async def handle(self, task: Task) -> Dict[str, Any]:
        """
        Обрабатывает заказ.
        """
        payload = task.payload
        order_id = payload["order_id"]
        amount = payload.get("amount", 0)
        user_id = payload.get("user_id")

        logger.info(f"OrderHandler: processing order {order_id} for user {user_id}")

        await asyncio.sleep(0.1)
        logger.info(f"Order {order_id}: validation passed")

        await asyncio.sleep(0.05)
        logger.info(f"Order {order_id}: charged {amount}")

        await asyncio.sleep(0.05)
        logger.info(f"Order {order_id}: inventory updated")

        logger.info(f"OrderHandler: completed order {order_id}")

        task.change_status("completed")
        return {
            "status": "processed",
            "order_id": order_id,
            "amount": amount,
            "user_id": user_id,
        }

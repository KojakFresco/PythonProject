from __future__ import annotations
from dataclasses import dataclass
import datetime

from task_platform.exceptions import (
    TaskStatusError,
    TaskPriorityError,
    TaskValidationError,
)


class ReadOnlyNonEmptyString:
    def __set_name__(self, owner, name):
        self.name = "_" + name

    def __get__(self, instance, owner):
        return getattr(instance, self.name, None)

    def __set__(self, instance, value):
        if hasattr(instance, self.name):
            raise AttributeError(f"{self.name[1:]} is read-only")
        if not isinstance(value, str):
            raise TypeError(f"{self.name[1:]} must be a string")
        if value.strip() == "":
            raise ValueError(f"{self.name[1:]} can not be empty")
        setattr(instance, self.name, value)


class ReadOnly:
    def __set_name__(self, owner, name):
        self.name = "_" + name

    def __get__(self, instance, owner):
        return getattr(instance, self.name, None)

    def __set__(self, instance, value):
        if hasattr(instance, self.name):
            raise AttributeError(f"{self.name[1:]} is read-only")
        setattr(instance, self.name, value)


class ReadOnlyDict:
    def __set_name__(self, owner, name):
        self.name = "_" + name

    def __get__(self, instance, owner):
        return getattr(instance, self.name, None)

    def __set__(self, instance, value):
        if hasattr(instance, self.name):
            raise AttributeError(f"{self.name[1:]} is read-only")
        if not isinstance(value, dict):
            raise TypeError(f"{self.name[1:]} must be a dictionary")
        setattr(instance, self.name, value)


class NonEmptyString:
    def __set_name__(self, owner, name):
        self.name = "_" + name

    def __get__(self, instance, owner):
        return getattr(instance, self.name, None)

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError(f"{self.name[1:]} must be a string")
        if value.strip() == "":
            raise ValueError(f"{self.name[1:]} can not be empty")
        setattr(instance, self.name, value)


class RangeInt:
    def __init__(self, low, high) -> None:
        self.low = low
        self.high = high

    def __set_name__(self, owner, name) -> None:
        self.name = "_" + name

    def __get__(self, instance, owner) -> int:
        return getattr(instance, self.name, None)

    def __set__(self, instance, value) -> None:
        if not isinstance(value, int):
            raise TypeError(f"{self.name[1:]} must be an integer")
        if not (self.low <= value <= self.high):
            raise ValueError(
                f"{self.name[1:]} must be an integer between {self.low} and {self.high}"
            )
        setattr(instance, self.name, value)


class AllowedValues:
    def __init__(self, *allowed) -> None:
        self.allowed = allowed

    def __set_name__(self, owner, name) -> None:
        self.name = "_" + name

    def __get__(self, instance, owner):
        return getattr(instance, self.name, None)

    def __set__(self, instance, value) -> None:
        if value not in self.allowed:
            raise ValueError(f"{self.name[1:]} must be one of {self.allowed}")
        setattr(instance, self.name, value)


class Task:
    id = ReadOnlyNonEmptyString()
    description = NonEmptyString()
    priority = RangeInt(1, 5)
    status = AllowedValues("pending", "in_progress", "completed")
    created_at = ReadOnly()
    payload = ReadOnlyDict()

    def __init__(
        self,
        id: str,
        description: str,
        priority: int = 1,
        status: str = "pending",
        payload: dict | None = None,
    ) -> None:
        try:
            self.id = id
            self.description = description
            self.priority = priority
            self.payload = payload or {}
            self.status = status
            self.created_at = datetime.datetime.now()
        except Exception as e:
            raise TaskValidationError(f"Invalid task data: {e}") from e

    def __str__(self) -> str:
        return f"Task(id={self.id}, description={self.description}, priority={self.priority}, status={self.status}, created_at={self.created_at})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Task):
            return NotImplemented
        return self.id == other.id

    def change_status(self, new_status: str) -> None:
        try:
            self.status = new_status
        except (TypeError, ValueError) as e:
            raise TaskStatusError(
                f"Invalid priority value: {e}. "
                f"Status must be one of 'pending', 'in_progress', or 'completed'"
            ) from e

    def change_priority(self, new_priority: int) -> None:
        try:
            self.priority = new_priority
        except (TypeError, ValueError) as e:
            raise TaskPriorityError(
                f"Invalid priority value: {e}. "
                f"Priority must be an integer between 1 and 5"
            ) from e

    @property
    def is_ready(self) -> bool:
        return self.status != "completed" and self.priority >= 3

    @classmethod
    def from_data(cls, task_data: TaskData) -> Task:
        raw_payload = task_data.payload

        clean_payload = {
            k: v
            for k, v in raw_payload.items()
            if k not in {"description", "priority", "status"}
        }

        return cls(
            id=task_data.id,
            description=raw_payload.get("description", ""),
            priority=raw_payload.get("priority", 1),
            status=raw_payload.get("status", "pending"),
            payload=clean_payload,
        )


@dataclass(frozen=True)
class TaskData:
    id: str
    payload: dict

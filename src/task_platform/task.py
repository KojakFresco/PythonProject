from __future__ import annotations
from dataclasses import dataclass
import datetime

from task_platform.exceptions import TaskStatusError, TaskPriorityError, TaskValidationError


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


class NotEmptyString:
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
    def __init__(self, low, high):
        self.low = low
        self.high = high

    def __set_name__(self, owner, name):
        self.name = "_" + name

    def __get__(self, instance, owner):
        return getattr(instance, self.name, None)

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError(f"{self.name[1:]} must be an integer")
        if not (self.low <= value <= self.high):
            raise ValueError(
                f"{self.name[1:]} must be an integer between {self.low} and {self.high}"
            )
        setattr(instance, self.name, value)


class AllowedValues:
    def __init__(self, *allowed):
        self.allowed = allowed

    def __set_name__(self, owner, name):
        self.name = "_" + name

    def __get__(self, instance, owner):
        return getattr(instance, self.name, None)

    def __set__(self, instance, value):
        if value not in self.allowed:
            raise ValueError(f"{self.name[1:]} must be one of {self.allowed}")
        setattr(instance, self.name, value)


class Task:
    id = ReadOnlyNonEmptyString()
    description = NotEmptyString()
    priority = RangeInt(1, 5)
    status = AllowedValues("pending", "in_progress", "completed")
    created_at = ReadOnly()

    def __init__(self, id: str, description: str, priority: int, status: str) -> None:
        try:
            self.id = id
            self.description = description
            self.priority = priority
            self.status = status
            self.created_at = datetime.datetime.now()
        except Exception as e:
            raise TaskValidationError(f"Invalid task data: {e}") from e

    @property
    def is_ready(self) -> bool:
        return self.status != "completed" and self.priority >= 3

    @classmethod
    def from_data(cls, task_data: TaskData) -> Task:
        payload = task_data.payload
        return cls(
            id=task_data.id,
            description=payload.get("description", ""),
            priority=int(payload.get("priority", 1)),
            status=payload.get("status", "pending"),
        )

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


@dataclass(frozen=True)
class TaskData:
    id: str
    payload: dict

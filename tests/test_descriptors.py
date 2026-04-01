import datetime

import pytest

from task_platform.task import AllowedValues, NotEmptyString, RangeInt, ReadOnly, ReadOnlyNonEmptyString, Task


def test_read_only_non_empty_string_descriptor_validation():
    descriptor = ReadOnlyNonEmptyString()
    descriptor.__set_name__(Task, "id")

    class Dummy:
        pass

    obj = Dummy()

    with pytest.raises(TypeError):
        descriptor.__set__(obj, 123)

    with pytest.raises(ValueError):
        descriptor.__set__(obj, "   ")

    descriptor.__set__(obj, "task-1")
    assert descriptor.__get__(obj, Dummy) == "task-1"

    with pytest.raises(AttributeError):
        descriptor.__set__(obj, "task-2")


def test_not_empty_string_descriptor_validation():
    descriptor = NotEmptyString()
    descriptor.__set_name__(Task, "description")

    class Dummy:
        pass

    obj = Dummy()

    with pytest.raises(TypeError):
        descriptor.__set__(obj, 123)

    with pytest.raises(ValueError):
        descriptor.__set__(obj, "")

    descriptor.__set__(obj, "hello")
    assert descriptor.__get__(obj, Dummy) == "hello"


def test_range_int_descriptor_validation():
    descriptor = RangeInt(1, 5)
    descriptor.__set_name__(Task, "priority")

    class Dummy:
        pass

    obj = Dummy()

    with pytest.raises(TypeError):
        descriptor.__set__(obj, "high")

    with pytest.raises(ValueError):
        descriptor.__set__(obj, 0)

    descriptor.__set__(obj, 3)
    assert descriptor.__get__(obj, Dummy) == 3


def test_allowed_values_descriptor_validation():
    descriptor = AllowedValues("pending", "in_progress", "completed")
    descriptor.__set_name__(Task, "status")

    class Dummy:
        pass

    obj = Dummy()

    with pytest.raises(ValueError):
        descriptor.__set__(obj, "invalid_status")

    descriptor.__set__(obj, "pending")
    assert descriptor.__get__(obj, Dummy) == "pending"


def test_read_only_descriptor_validation():
    descriptor = ReadOnly()
    descriptor.__set_name__(Task, "created_at")

    class Dummy:
        pass

    obj = Dummy()
    now = datetime.datetime.now()

    descriptor.__set__(obj, now)
    assert descriptor.__get__(obj, Dummy) == now

    with pytest.raises(AttributeError):
        descriptor.__set__(obj, datetime.datetime.now())


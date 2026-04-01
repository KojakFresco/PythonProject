from task_platform.protocols import TaskSource
from task_platform.task import TaskData


def collect_tasks(source: TaskSource) -> list[TaskData]:

    if not isinstance(source, TaskSource):
        raise TypeError("Object does not implement TaskSource")

    return list(source.get_tasks())

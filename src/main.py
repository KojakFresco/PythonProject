from task_platform.collector import collect_tasks
from task_platform.sources.generator_source import GeneratorTaskSource
from task_platform.sources.api_source import ApiTaskSource
from task_platform.task import Task
from task_platform.task_queue import TaskQueue


def main():
    # print(collect_tasks(GeneratorTaskSource(5)))
    # print(collect_tasks(ApiTaskSource("http://127.0.0.1:8000/tasks")))
    task_queue = TaskQueue()
    task_queue.from_source(GeneratorTaskSource(6))

    for task in task_queue.filter_by_priority(1):
        print(task)
    print(sum(task_queue))


if __name__ == "__main__":
    main()

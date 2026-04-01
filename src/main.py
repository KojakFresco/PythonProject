from task_platform.collector import collect_tasks
from task_platform.sources.generator_source import GeneratorTaskSource
from task_platform.sources.api_source import ApiTaskSource


def main():
    print(collect_tasks(GeneratorTaskSource(5)))
    print(collect_tasks(ApiTaskSource("http://127.0.0.1:8000/tasks")))


if __name__ == "__main__":
    main()

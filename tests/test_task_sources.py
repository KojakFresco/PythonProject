from pyfakefs.fake_filesystem import FakeFilesystem
from unittest.mock import patch, Mock

from task_platform.sources.file_source import FileTaskSource
from task_platform.sources.generator_source import GeneratorTaskSource
from task_platform.task import TaskData
from task_platform.sources.api_source import ApiTaskSource


def test_file_source(fs: FakeFilesystem):
    fs.create_file(
        "new",
        contents='[{"id": "id-1", "payload": {"type": "email", "user": 10}}, {"id": "id-2", "payload": {"type": "order", "order_id": 42}}]',
    )
    file_task_source = FileTaskSource("new")
    print(type(list(file_task_source.get_tasks())[0]))
    print(type(TaskData(id="id-1", payload={"type": "email", "user": 10})))

    assert list(file_task_source.get_tasks()) == [
        TaskData(id="id-1", payload={"type": "email", "user": 10}),
        TaskData(id="id-2", payload={"type": "order", "order_id": 42}),
    ]


def test_generator_source():
    generator_task_source = GeneratorTaskSource(5)
    tasks = list(generator_task_source.get_tasks())
    assert len(tasks) == 5


def test_api_source():
    fake_data = [
        {"id": "id-1", "payload": {"type": "email"}},
        {"id": "id-2", "payload": {"type": "order"}},
    ]

    mock_response = Mock()
    mock_response.json.return_value = fake_data

    with patch("requests.get", return_value=mock_response):
        source = ApiTaskSource("http://fake-api/tasks")

        tasks = list(source.get_tasks())

        assert tasks == [
            TaskData(id="id-1", payload={"type": "email"}),
            TaskData(id="id-2", payload={"type": "order"}),
        ]

from typing import List
from src.app_data import get_data_file_path
from src.task import Task
from src.json_file import StorageError, read_json, write_json


class TaskFileStorage:
    """Handles loading and saving tasks to a JSON file."""

    FILENAME = "todos.json"

    KEY_TEXT = "text"
    KEY_DONE = "done"
    KEY_CREATED_AT = "created_at"
    KEY_COMPLETED_AT = "completed_at"
    KEY_ORDER = "order"
    KEY_DAILY = "daily"

    @staticmethod
    def get_file_path() -> str:
        return get_data_file_path(TaskFileStorage.FILENAME)

    @staticmethod
    def load_tasks() -> List[Task]:
        file_path = TaskFileStorage.get_file_path()
        data = read_json(file_path, [])
        try:
            if not isinstance(data, list):
                raise ValueError("Expected a list of tasks")
            tasks = []
            for index, item in enumerate(data):
                if not isinstance(item, dict):
                    raise ValueError("Expected a task object")
                if not isinstance(item.get(TaskFileStorage.KEY_TEXT), str):
                    raise ValueError("Task text must be a string")
                if not isinstance(item.get(TaskFileStorage.KEY_DONE), bool):
                    raise ValueError("Task completion must be a boolean")
                if not isinstance(item.get(TaskFileStorage.KEY_DAILY, False), bool):
                    raise ValueError("Daily task status must be a boolean")
                for key in (TaskFileStorage.KEY_CREATED_AT, TaskFileStorage.KEY_COMPLETED_AT):
                    if item.get(key) is not None and not isinstance(item[key], str):
                        raise ValueError(f"Task {key} must be a string or null")
                order = item.get(TaskFileStorage.KEY_ORDER)
                tasks.append(Task(
                    text=item[TaskFileStorage.KEY_TEXT],
                    done=item[TaskFileStorage.KEY_DONE],
                    created_at=item.get(TaskFileStorage.KEY_CREATED_AT),
                    completed_at=item.get(TaskFileStorage.KEY_COMPLETED_AT),
                    order=index if order is None else order,
                    daily=item.get(TaskFileStorage.KEY_DAILY, False),
                ))
            return tasks
        except (TypeError, ValueError, OverflowError) as error:
            raise StorageError(file_path, "read", str(error)) from error

    @staticmethod
    def save_tasks(tasks: List[Task]) -> None:
        file_path = TaskFileStorage.get_file_path()

        data = [
            {
                TaskFileStorage.KEY_TEXT: task.text,
                TaskFileStorage.KEY_DONE: task.done,
                TaskFileStorage.KEY_CREATED_AT: task.created_at,
                TaskFileStorage.KEY_COMPLETED_AT: task.completed_at,
                TaskFileStorage.KEY_ORDER: task.order,
                TaskFileStorage.KEY_DAILY: task.daily,
            }
            for task in tasks
        ]

        write_json(file_path, data)

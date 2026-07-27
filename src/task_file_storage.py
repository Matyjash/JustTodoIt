import json
import os
from datetime import datetime
from typing import List
from src.app_data import get_data_file_path
from src.task import Task


class TaskFileStorage:
    """Handles loading and saving tasks to a JSON file."""

    FILENAME = "todos.json"

    KEY_TEXT = "text"
    KEY_DONE = "done"
    KEY_CREATED_AT = "created_at"
    KEY_COMPLETED_AT = "completed_at"
    KEY_ORDER = "order"

    @staticmethod
    def get_file_path() -> str:
        return get_data_file_path(TaskFileStorage.FILENAME)

    @staticmethod
    def _normalize_task_orders(tasks: List[Task]) -> None:
        for index, task in enumerate(tasks):
            task.order = index

    @staticmethod
    def load_tasks() -> List[Task]:
        file_path = TaskFileStorage.get_file_path()

        if not os.path.exists(file_path):
            return []

        try:
            with open(file_path, "r") as f:
                data = json.load(f)
                tasks = []
                for index, item in enumerate(data):
                    created_at = item.get(TaskFileStorage.KEY_CREATED_AT)
                    if not created_at:
                        created_at = datetime.now().strftime(Task.TIME_FORMAT)
                    order = item.get(TaskFileStorage.KEY_ORDER)
                    if order is None:
                        order = index
                    task = Task(
                        text=item[TaskFileStorage.KEY_TEXT],
                        done=item[TaskFileStorage.KEY_DONE],
                        created_at=created_at,
                        completed_at=item.get(TaskFileStorage.KEY_COMPLETED_AT),
                        order=order,
                    )
                    tasks.append(task)
                TaskFileStorage._normalize_task_orders(tasks)
                return tasks
        except (json.JSONDecodeError, KeyError, IOError):
            return []

    @staticmethod
    def save_tasks(tasks: List[Task]) -> None:
        file_path = TaskFileStorage.get_file_path()

        TaskFileStorage._normalize_task_orders(tasks)

        data = [
            {
                TaskFileStorage.KEY_TEXT: task.text,
                TaskFileStorage.KEY_DONE: task.done,
                TaskFileStorage.KEY_CREATED_AT: task.created_at,
                TaskFileStorage.KEY_COMPLETED_AT: task.completed_at,
                TaskFileStorage.KEY_ORDER: task.order,
            }
            for task in tasks
        ]

        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w") as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            print(f"Error saving tasks: {e}")

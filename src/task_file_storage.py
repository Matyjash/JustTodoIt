import json
import os
from datetime import datetime
from typing import List
from src.task import Task


class TaskFileStorage:
    """Handles loading and saving tasks to a JSON file."""

    FILENAME = "todos.json"

    KEY_TEXT = "text"
    KEY_DONE = "done"
    KEY_CREATED_AT = "created_at"
    KEY_COMPLETED_AT = "completed_at"

    @staticmethod
    def get_file_path() -> str:
        app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(app_dir, TaskFileStorage.FILENAME)

    @staticmethod
    def load_tasks() -> List[Task]:
        file_path = TaskFileStorage.get_file_path()

        if not os.path.exists(file_path):
            return []

        try:
            with open(file_path, "r") as f:
                data = json.load(f)
                tasks = []
                for item in data:
                    created_at = item.get(TaskFileStorage.KEY_CREATED_AT)
                    if not created_at:
                        created_at = datetime.now().strftime(Task.TIME_FORMAT)
                    task = Task(
                        text=item[TaskFileStorage.KEY_TEXT],
                        done=item[TaskFileStorage.KEY_DONE],
                        created_at=created_at,
                        completed_at=item.get(TaskFileStorage.KEY_COMPLETED_AT)
                    )
                    tasks.append(task)
                return tasks
        except (json.JSONDecodeError, KeyError, IOError):
            return []

    @staticmethod
    def save_tasks(tasks: List[Task]) -> None:
        file_path = TaskFileStorage.get_file_path()

        data = [
            {
                TaskFileStorage.KEY_TEXT: task.text,
                TaskFileStorage.KEY_DONE: task.done,
                TaskFileStorage.KEY_CREATED_AT: task.created_at,
                TaskFileStorage.KEY_COMPLETED_AT: task.completed_at
            }
            for task in tasks
        ]

        try:
            with open(file_path, "w") as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            print(f"Error saving tasks: {e}")

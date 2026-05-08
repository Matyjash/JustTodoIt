import json
import os
from typing import List
from src.task import Task


class TaskFileStorage:
    """Handles loading and saving tasks to a JSON file."""

    FILENAME = "todos.json"

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
                tasks = [Task(text=item["text"], done=item["done"]) for item in data]
                return tasks
        except (json.JSONDecodeError, KeyError, IOError):
            return []

    @staticmethod
    def save_tasks(tasks: List[Task]) -> None:
        file_path = TaskFileStorage.get_file_path()

        data = [{"text": task.text, "done": task.done} for task in tasks]

        try:
            with open(file_path, "w") as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            print(f"Error saving tasks: {e}")

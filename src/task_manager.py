from typing import Iterable, Protocol

from src.task import Task


class TaskStorage(Protocol):
    def load_tasks(self) -> list[Task]: ...

    def save_tasks(self, tasks: list[Task]) -> None: ...


class TaskManager:
    def __init__(self, storage: TaskStorage):
        self._storage = storage
        self._tasks = list(storage.load_tasks())
        self._normalize_orders()

    @property
    def tasks(self) -> tuple[Task, ...]:
        return tuple(self._tasks)

    def add(self, text: str) -> Task | None:
        text = text.strip()
        if not text:
            return None
        task = Task(text=text)
        self._tasks.append(task)
        self._save()
        return task

    def rename(self, task: Task, text: str) -> bool:
        text = text.strip()
        if task not in self._tasks or not text or task.text == text:
            return False
        task.text = text
        self._save()
        return True

    def toggle(self, task: Task) -> bool:
        if task not in self._tasks:
            return False
        task.toggle()
        self._save()
        return True

    def remove(self, tasks: Iterable[Task]) -> bool:
        selected = set(tasks)
        remaining = [task for task in self._tasks if task not in selected]
        if len(remaining) == len(self._tasks):
            return False
        self._tasks = remaining
        self._save()
        return True

    def clear(self) -> None:
        if self._tasks:
            self._tasks.clear()
            self._save()

    def move(self, from_index: int, insertion_index: int) -> bool:
        if not 0 <= from_index < len(self._tasks):
            return False
        destination = max(0, min(insertion_index, len(self._tasks)))
        if destination > from_index:
            destination -= 1
        if destination == from_index:
            return False
        task = self._tasks.pop(from_index)
        self._tasks.insert(destination, task)
        self._save()
        return True

    def _normalize_orders(self) -> None:
        for index, task in enumerate(self._tasks):
            task.order = index

    def _save(self) -> None:
        self._normalize_orders()
        self._storage.save_tasks(list(self._tasks))

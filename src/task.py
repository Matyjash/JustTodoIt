from datetime import datetime
from typing import Optional


class Task:
    TIME_FORMAT = "%Y-%m-%d %H:%M"

    def __init__(self, text: str, done: bool = False, created_at: Optional[str] = None, completed_at: Optional[str] = None):
        self.text = text
        self.done = done
        self.created_at = created_at if created_at else datetime.now().strftime(Task.TIME_FORMAT)
        self.completed_at = completed_at

    def toggle(self):
        self.done = not self.done
        if self.done:
            self.completed_at = datetime.now().strftime(Task.TIME_FORMAT)

    def __str__(self):
        status = "[x]" if self.done else "☐"
        return f"{status} {self.text}"

    def __repr__(self):
        return f"Task(text='{self.text}', done={self.done})"

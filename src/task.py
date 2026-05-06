class Task:
    def __init__(self, text: str, done: bool = False):
        """
        Initialize a Task.

        Args:
            text: The task description
            done: Whether the task is completed (default: False)
        """
        self.text = text
        self.done = done

    def toggle(self):
        self.done = not self.done

    def __str__(self):
        status = "[x]" if self.done else "☐"
        return f"{status} {self.text}"

    def __repr__(self):
        return f"Task(text='{self.text}', done={self.done})"

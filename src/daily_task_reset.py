from collections.abc import Callable, Iterable
from datetime import datetime, time, timedelta

from src.task import Task


class DailyTaskReset:
    """Resets daily completions older than the latest local reset boundary."""

    def __init__(self, reset_time: Callable[[], time] = time, clock: Callable[[], datetime] = datetime.now):
        self._reset_time = reset_time
        self._clock = clock

    def reset(self, tasks: Iterable[Task]) -> bool:
        now = self._clock()
        boundary = datetime.combine(now.date(), self._reset_time())
        if now < boundary:
            boundary -= timedelta(days=1)
        changed = False
        for task in tasks:
            if not task.daily or not task.done:
                continue
            try:
                completed = datetime.strptime(task.completed_at, Task.TIME_FORMAT)
            except (TypeError, ValueError):
                completed = datetime.min
            if completed < boundary:
                task.done = False
                task.completed_at = None
                changed = True
        return changed

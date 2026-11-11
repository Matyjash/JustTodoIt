from pathlib import Path

from PyQt5.QtCore import QLockFile

from src.json_file import StorageError


class SingleInstanceLock:
    def __init__(self, path: str):
        self.path = Path(path)
        self._lock = QLockFile(str(self.path))
        self._lock.setStaleLockTime(0)

    def acquire(self) -> bool:
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
        except OSError as error:
            raise StorageError(self.path, "lock", str(error)) from error
        if self._lock.tryLock(0):
            return True
        if self._lock.error() == QLockFile.LockFailedError:
            return False
        reason = (
            "Permission denied"
            if self._lock.error() == QLockFile.PermissionError
            else "Unable to create the application lock"
        )
        raise StorageError(self.path, "lock", reason)

    def release(self) -> None:
        self._lock.unlock()

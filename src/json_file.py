import json
import os
from pathlib import Path
import tempfile


class StorageError(Exception):
    def __init__(self, path: str | Path, operation: str, reason: str):
        self.path = str(path)
        self.operation = operation
        super().__init__(f"Could not {operation} {self.path}: {reason}")


def read_json(path: str | Path, default):
    try:
        with open(path, encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return default
    except (OSError, UnicodeError, ValueError) as error:
        raise StorageError(path, "read", str(error)) from error


def write_json(path: str | Path, data) -> None:
    path = Path(path)
    temporary_path = None
    try:
        contents = json.dumps(data, indent=2, ensure_ascii=True, allow_nan=False)
        path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent,
            prefix=f".{path.name}.", suffix=".tmp", delete=False,
        ) as file:
            temporary_path = Path(file.name)
            file.write(contents)
            file.flush()
            os.fsync(file.fileno())
        os.replace(temporary_path, path)
    except (OSError, TypeError, ValueError, UnicodeError) as error:
        raise StorageError(path, "save", str(error)) from error
    finally:
        if temporary_path is not None:
            try:
                temporary_path.unlink(missing_ok=True)
            except OSError:
                pass

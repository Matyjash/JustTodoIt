import re

from PyQt5.QtCore import QUrl


def validate_uri(value: str) -> str:
    uri = value.strip()
    url = QUrl(uri, QUrl.StrictMode)
    if (
        not uri
        or any(character.isspace() or ord(character) < 32 or ord(character) == 127 for character in uri)
        or not re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", uri)
        or not url.isValid()
        or url.isRelative()
        or (url.scheme().lower() in ("http", "https") and not url.host())
    ):
        raise ValueError("This is not a valid URI. Enter a complete URI, such as https://www.udemy.com/course/your-course/.")
    return uri

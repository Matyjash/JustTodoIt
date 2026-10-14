"""Scalable monochrome icons; colors accept Qt names, hex RGB, or QColor."""

from pathlib import Path

from PyQt5.QtCore import QByteArray, Qt
from PyQt5.QtGui import QColor, QIcon, QPainter, QPixmap
from PyQt5.QtSvg import QSvgRenderer


# PyInstaller preserves this module's path relative to the bundle root.
_ICONS_DIR = Path(__file__).resolve().parents[2] / "data" / "icons"
_ICON_FILES = {"settings": "settings.svg", "edit": "edit.svg"}


def create_icon(name: str, color: str | QColor) -> QIcon:
    """Tint an icon, e.g. create_icon('edit', QColor(30, 120, 210))."""
    tint = QColor(color)
    if not tint.isValid():
        raise ValueError(f"Invalid icon color: {color!r}")
    svg = (_ICONS_DIR / _ICON_FILES[name]).read_text(encoding="utf-8")
    svg = svg.replace("currentColor", tint.name())
    renderer = QSvgRenderer(QByteArray(svg.encode("utf-8")))
    icon = QIcon()
    # Include larger rasters so Qt can select a sharp image on high-DPI screens.
    for size in (16, 18, 20, 24, 32, 36, 40, 48, 64):
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setOpacity(tint.alphaF())
        renderer.render(painter)
        painter.end()
        icon.addPixmap(pixmap)
    return icon

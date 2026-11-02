from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from PyQt5.QtCore import QSettings, QSize, Qt
from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication

from src.settings.settings_storage import SettingsStorage
from src.settings.theme import ThemeSettings
from src.task_file_storage import TaskFileStorage
from src.task_manager import TaskManager
from src.ui.main_window import MainWindow
from src.ui.theme.theme import TIGER_THEME_NAME


CAPTURE_SIZE = QSize(309, 442)
CAPTURE_DELAY_MS = 150
CAPTURE_DEVICE_PIXEL_RATIO = 1

PREVIEW_TASK_TEXT = "develop this app"
PREVIEW_THEME_NAME = TIGER_THEME_NAME

WINDOW_SETTINGS_FILENAME = "window.ini"
PREVIEW_PATH = Path(__file__).resolve().parent / "docs" / "app_preview.png"


def capture(app, add_task=False):
    window = MainWindow(
        TaskManager(TaskFileStorage()), ThemeSettings.load_selected_theme()
    )
    window.resize(CAPTURE_SIZE)
    window.display()
    if add_task:
        window.input_field.setText(PREVIEW_TASK_TEXT)
        window.add_todo()
    window.input_field.clearFocus()
    QTest.qWait(CAPTURE_DELAY_MS)
    app.processEvents()
    screenshot = window.grab().toImage()
    screenshot.setDevicePixelRatio(CAPTURE_DEVICE_PIXEL_RATIO)
    screenshot = screenshot.scaled(CAPTURE_SIZE, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
    window.close()
    return screenshot


def main():
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)
    with TemporaryDirectory() as directory:
        geometry = QSettings(str(Path(directory) / WINDOW_SETTINGS_FILENAME), QSettings.IniFormat)
        with patch("src.app_data.get_app_data_dir", return_value=directory), patch(
            "src.ui.base_window.QSettings", return_value=geometry
        ):
            default = capture(app, add_task=True)
            ThemeSettings.select_theme(SettingsStorage.load_settings(), PREVIEW_THEME_NAME)
            tiger = capture(app)

    screenshots = (tiger, default)
    preview = QImage(
        CAPTURE_SIZE.width() * len(screenshots), CAPTURE_SIZE.height(), QImage.Format_RGB32
    )
    painter = QPainter(preview)
    for index, screenshot in enumerate(screenshots):
        painter.drawImage(index * CAPTURE_SIZE.width(), 0, screenshot)
    painter.end()
    if not preview.save(str(PREVIEW_PATH)):
        raise OSError(f"Could not save {PREVIEW_PATH}")
    print(f"Saved {PREVIEW_PATH}")


if __name__ == "__main__":
    main()

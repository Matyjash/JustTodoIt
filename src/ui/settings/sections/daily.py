from PyQt5.QtCore import QTime
from PyQt5.QtWidgets import QLabel, QTimeEdit

from src.settings.daily import DailySettings
from src.settings.settings_storage import SettingsStorage
from src.ui.settings.sections.setting import Setting
from src.ui.theme.theme import Theme


class Daily(Setting):
    """Provides the local time at which daily tasks become unfinished."""

    def __init__(self, settings: dict, theme: Theme):
        self.settings = settings
        self.theme = theme

    def is_available(self) -> bool:
        return True

    def add_to_layout(self, layout) -> None:
        label = QLabel("Reset daily ToDos at (local time):")
        label.setStyleSheet(f"color: {self.theme.text_color};")
        layout.addWidget(label)
        reset_time = DailySettings.reset_time(self.settings)
        selector = QTimeEdit(QTime(reset_time.hour, reset_time.minute))
        selector.setDisplayFormat("HH:mm")
        selector.setStyleSheet(f"color: {self.theme.text_color}; background-color: {self.theme.surface_color};")
        selector.timeChanged.connect(self._on_time_changed)
        layout.addWidget(selector)

    def _on_time_changed(self, value: QTime) -> None:
        self.settings[DailySettings.RESET_TIME_KEY] = value.toString("HH:mm")
        SettingsStorage.save_settings(self.settings)

from PyQt5.QtCore import QTime
from PyQt5.QtWidgets import QTimeEdit

from src.settings.daily import DailySettings
from src.settings.settings_storage import SettingsStorage
from src.ui.settings.sections.setting import Setting


class Daily(Setting):
    """Provides the local time at which daily tasks become unfinished."""

    def __init__(self, settings: dict):
        self.settings = settings

    def is_available(self) -> bool:
        return True

    def add_to_layout(self, layout) -> None:
        content = self.create_section(layout, "Daily tasks")
        reset_time = DailySettings.reset_time(self.settings)
        selector = QTimeEdit(QTime(reset_time.hour, reset_time.minute))
        selector.setDisplayFormat("HH:mm")
        selector.timeChanged.connect(self._on_time_changed)
        self.add_control(content, "Reset time", selector)
        self.add_description(content, "Daily ToDos become unfinished at this local time.")

    def _on_time_changed(self, value: QTime) -> None:
        self.settings[DailySettings.RESET_TIME_KEY] = value.toString("HH:mm")
        SettingsStorage.save_settings(self.settings)

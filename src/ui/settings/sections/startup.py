from PyQt5.QtWidgets import QCheckBox, QLabel
from src.settings.settings_storage import SettingsStorage
from src.settings.startup import Startup as StartupService
from src.ui.settings.sections.setting import Setting
from src.ui.theme.theme import Theme


SETTING_KEY = "startup"
SECTION_LABEL = "Launch on system boot:"
CHECKBOX_LABEL = "Enable"
SUPPORTED_INFO_LABEL = "Starts JustTodoIt automatically when you sign in to Windows."
UNSUPPORTED_INFO_LABEL = "Available in the packaged Windows application."
INFO_LABEL_FONT_SIZE = "9pt"


class Startup(Setting):
    """Provides the startup setting when the installed app supports it."""

    def __init__(self, settings: dict, theme: Theme):
        self.settings = settings
        self.theme = theme
        self.startup_service = StartupService()

    def is_available(self) -> bool:
        return self.startup_service.is_windows()

    def add_to_layout(self, layout) -> None:
        section_label = QLabel(SECTION_LABEL)
        section_label.setStyleSheet(f"color: {self.theme.text_color};")
        layout.addWidget(section_label)

        checkbox = QCheckBox(CHECKBOX_LABEL)
        checkbox.setStyleSheet(f"color: {self.theme.text_color};")
        checkbox.setChecked(self.settings.get(SETTING_KEY, False))
        checkbox.setEnabled(self.startup_service.is_supported())
        checkbox.stateChanged.connect(self._on_state_changed)
        layout.addWidget(checkbox)

        info_label = QLabel(self._get_info_label())
        info_label.setStyleSheet(
            f"color: {self.theme.text_color}; font-size: {INFO_LABEL_FONT_SIZE};"
        )
        layout.addWidget(info_label)

    def _on_state_changed(self, state: int) -> None:
        is_enabled = bool(state)
        self.settings[SETTING_KEY] = is_enabled
        SettingsStorage.save_settings(self.settings)

        if is_enabled:
            self.startup_service.enable()
        else:
            self.startup_service.disable()

    def _get_info_label(self) -> str:
        if self.startup_service.is_supported():
            return SUPPORTED_INFO_LABEL
        return UNSUPPORTED_INFO_LABEL

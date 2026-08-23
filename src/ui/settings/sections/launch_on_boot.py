from PyQt5.QtWidgets import QCheckBox, QLabel
from src.settings.settings_storage import SettingsStorage
from src.ui.settings.sections.setting import Setting
from src.ui.settings.sections.startup import StartupManager
from src.ui.style import Style


SETTING_KEY = "launch_on_boot"
SECTION_LABEL = "Launch on system boot:"
CHECKBOX_LABEL = "Enable"
SUPPORTED_INFO_LABEL = "Starts JustTodoIt automatically when you sign in to Windows."
UNSUPPORTED_INFO_LABEL = "Available in the packaged Windows application."
INFO_LABEL_FONT_SIZE = "9pt"
INFO_LABEL_TEXT_COLOR = "gray"


class LaunchOnBoot(Setting):
    """Provides the launch-on-boot setting when the installed app supports it."""

    def __init__(self, settings: dict, style: Style):
        self.settings = settings
        self.style = style
        self.startup_manager = StartupManager()

    def is_available(self) -> bool:
        return self.startup_manager.is_windows()

    def add_to_layout(self, layout) -> None:
        layout.addWidget(QLabel(SECTION_LABEL))

        checkbox = QCheckBox(CHECKBOX_LABEL)
        checkbox.setChecked(self.settings.get(SETTING_KEY, False))
        checkbox.setEnabled(self.startup_manager.is_supported())
        checkbox.stateChanged.connect(self._on_state_changed)
        layout.addWidget(checkbox)

        info_label = QLabel(self._get_info_label())
        info_label.setStyleSheet(
            f"color: {INFO_LABEL_TEXT_COLOR}; font-size: {INFO_LABEL_FONT_SIZE};"
        )
        layout.addWidget(info_label)

    def _on_state_changed(self, state: int) -> None:
        is_enabled = bool(state)
        self.settings[SETTING_KEY] = is_enabled
        SettingsStorage.save_settings(self.settings)

        if is_enabled:
            self.startup_manager.enable()
        else:
            self.startup_manager.disable()

    def _get_info_label(self) -> str:
        if self.startup_manager.is_supported():
            return SUPPORTED_INFO_LABEL
        return UNSUPPORTED_INFO_LABEL

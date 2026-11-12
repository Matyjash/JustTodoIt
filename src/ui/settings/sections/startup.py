from src.ui.components.checkbox import ThemedCheckBox
from src.settings.settings_storage import SettingsStorage
from src.settings.startup import Startup as StartupService
from src.ui.settings.sections.setting import Setting
from src.ui.theme.theme import Theme


SETTING_KEY = "startup"
SECTION_LABEL = "Startup"
CHECKBOX_LABEL = "Launch at sign-in"
SUPPORTED_INFO_LABEL = "Open JustTodoIt automatically when you sign in to Windows."
UNSUPPORTED_INFO_LABEL = "Available in the packaged Windows application."


class Startup(Setting):
    """Provides the startup setting when the installed app supports it."""

    def __init__(self, settings: dict, theme: Theme):
        self.settings = settings
        self.theme = theme
        self.startup_service = StartupService()

    def is_available(self) -> bool:
        return self.startup_service.is_windows()

    def add_to_layout(self, layout) -> None:
        content = self.create_section(layout, SECTION_LABEL)

        checkbox = ThemedCheckBox(self.theme, CHECKBOX_LABEL)

        checkbox.setChecked(self.settings.get(SETTING_KEY, False))
        checkbox.setEnabled(self.startup_service.is_supported())
        checkbox.stateChanged.connect(self._on_state_changed)
        checkbox.setMinimumHeight(26)
        content.addWidget(checkbox)
        self.add_description(content, self._get_info_label())

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

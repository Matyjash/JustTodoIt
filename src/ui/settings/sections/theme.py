from collections.abc import Callable
from PyQt5.QtWidgets import QComboBox
from src.settings.theme import ThemeSettings
from src.ui.settings.sections.setting import Setting
from src.ui.theme.theme import Theme as ThemeConfiguration


SECTION_LABEL = "Appearance"


class Theme(Setting):
    """Provides a selector for the application's visual theme."""

    def __init__(
        self,
        settings: dict,
        on_theme_changed: Callable[[ThemeConfiguration], None],
    ):
        self.settings = settings
        self.on_theme_changed = on_theme_changed

    def is_available(self) -> bool:
        return True

    def add_to_layout(self, layout) -> None:
        content = self.create_section(layout, SECTION_LABEL)

        theme_selector = QComboBox()
        theme_selector.addItems(ThemeSettings.get_available_theme_names())
        theme_selector.setCurrentText(ThemeSettings.get_selected_theme_name(self.settings))
        theme_selector.currentTextChanged.connect(self._on_theme_changed)
        self.add_control(content, "Theme", theme_selector)

    def _on_theme_changed(self, theme_name: str) -> None:
        theme = ThemeSettings.select_theme(self.settings, theme_name)
        self.on_theme_changed(theme)

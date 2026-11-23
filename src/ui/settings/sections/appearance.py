from collections.abc import Callable
from PyQt5.QtWidgets import QComboBox
from src.settings.theme import ThemeSettings
from src.settings.font import FontSettings
from src.ui.settings.sections.setting import Setting
from src.ui.theme.theme import Theme as ThemeConfiguration


SECTION_LABEL = "Appearance"


class Appearance(Setting):
    """Provides selectors for the application's theme and font."""

    def __init__(
        self,
        settings: dict,
        on_theme_changed: Callable[[ThemeConfiguration], None],
        on_font_changed: Callable[[str], None],
    ):
        self.settings = settings
        self.on_theme_changed = on_theme_changed
        self.on_font_changed = on_font_changed

    def is_available(self) -> bool:
        return True

    def add_to_layout(self, layout) -> None:
        content = self.create_section(layout, SECTION_LABEL)

        theme_selector = QComboBox()
        theme_selector.addItems(ThemeSettings.get_available_theme_names())
        theme_selector.setCurrentText(ThemeSettings.get_selected_theme_name(self.settings))
        theme_selector.currentTextChanged.connect(self._on_theme_changed)
        self.add_control(content, "Theme", theme_selector)

        font_selector = QComboBox()
        font_selector.addItems(FontSettings.get_available_font_names())
        font_selector.setCurrentText(FontSettings.get_selected_font_name(self.settings))
        font_selector.currentTextChanged.connect(self._on_font_changed)
        self.add_control(content, "Font", font_selector)

    def _on_font_changed(self, font_name: str) -> None:
        font = FontSettings.select_font(self.settings, font_name)
        self.on_font_changed(font)

    def _on_theme_changed(self, theme_name: str) -> None:
        theme = ThemeSettings.select_theme(self.settings, theme_name)
        self.on_theme_changed(theme)

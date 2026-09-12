from collections.abc import Callable
from PyQt5.QtWidgets import QComboBox, QLabel
from src.settings.theme import ThemeSettings
from src.ui.settings.sections.setting import Setting
from src.ui.theme.theme import Theme as ThemeConfiguration


SECTION_LABEL = "Theme:"


class Theme(Setting):
    """Provides a selector for the application's visual theme."""

    def __init__(
        self,
        settings: dict,
        theme: ThemeConfiguration,
        on_theme_changed: Callable[[ThemeConfiguration], None],
    ):
        self.settings = settings
        self.theme = theme
        self.on_theme_changed = on_theme_changed

    def is_available(self) -> bool:
        return True

    def add_to_layout(self, layout) -> None:
        section_label = QLabel(SECTION_LABEL)
        section_label.setStyleSheet(f"color: {self.theme.text_color};")
        layout.addWidget(section_label)

        theme_selector = QComboBox()
        theme_selector.addItems(ThemeSettings.get_available_theme_names())
        theme_selector.setCurrentText(ThemeSettings.get_selected_theme_name(self.settings))
        theme_selector.setStyleSheet(
            f"QComboBox {{ color: {self.theme.text_color}; background-color: {self.theme.surface_color}; "
            f"border: 1px solid {self.theme.border_color}; }}"
            f"QComboBox QAbstractItemView {{ color: {self.theme.text_color}; background-color: {self.theme.surface_color}; "
            f"selection-background-color: {self.theme.background_color}; }}"
        )
        theme_selector.currentTextChanged.connect(self._on_theme_changed)
        layout.addWidget(theme_selector)

    def _on_theme_changed(self, theme_name: str) -> None:
        theme = ThemeSettings.select_theme(self.settings, theme_name)
        self.on_theme_changed(theme)

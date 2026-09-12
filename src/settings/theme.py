from src.settings.settings_storage import SettingsStorage
from src.ui.theme.theme import DEFAULT_THEME, DEFAULT_THEME_NAME, THEMES, Theme


THEME_SETTING_KEY = "theme"


class ThemeSettings:
    """Manages available themes and the selected theme setting."""

    @staticmethod
    def get_available_theme_names() -> tuple[str, ...]:
        return tuple(THEMES.keys())

    @staticmethod
    def load_selected_theme() -> Theme:
        settings = SettingsStorage.load_settings()
        return ThemeSettings.get_theme(settings.get(THEME_SETTING_KEY))

    @staticmethod
    def select_theme(settings: dict, theme_name: str) -> Theme:
        theme = ThemeSettings.get_theme(theme_name)
        settings[THEME_SETTING_KEY] = theme_name
        SettingsStorage.save_settings(settings)
        return theme

    @staticmethod
    def get_selected_theme_name(settings: dict) -> str:
        theme_name = settings.get(THEME_SETTING_KEY, DEFAULT_THEME_NAME)
        if theme_name in THEMES:
            return theme_name
        return DEFAULT_THEME_NAME

    @staticmethod
    def get_theme(theme_name: str | None) -> Theme:
        return THEMES.get(theme_name, DEFAULT_THEME)

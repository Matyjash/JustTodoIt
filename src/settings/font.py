from src.settings.settings_storage import SettingsStorage


FONT_SETTING_KEY = "font"
DEFAULT_FONT_NAME = "Arial"
FONT_NAMES = (DEFAULT_FONT_NAME, "Segoe UI")


class FontSettings:
    """Manages available font families and the persisted selection."""

    @staticmethod
    def get_available_font_names() -> tuple[str, ...]:
        return FONT_NAMES

    @staticmethod
    def load_selected_font() -> str:
        return FontSettings.get_selected_font_name(SettingsStorage.load_settings())

    @staticmethod
    def get_selected_font_name(settings: dict) -> str:
        font_name = settings.get(FONT_SETTING_KEY, DEFAULT_FONT_NAME)
        return font_name if font_name in FONT_NAMES else DEFAULT_FONT_NAME

    @staticmethod
    def select_font(settings: dict, font_name: str) -> str:
        selected_font = FontSettings.get_selected_font_name({FONT_SETTING_KEY: font_name})
        settings[FONT_SETTING_KEY] = selected_font
        SettingsStorage.save_settings(settings)
        return selected_font

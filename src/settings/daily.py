from datetime import datetime, time

from src.settings.settings_storage import SettingsStorage


class DailySettings:
    """Loads the local daily reset time and daily list preferences."""

    RESET_TIME_KEY = "daily_reset_time"
    SHOW_DAILY_KEY = "show_daily"
    ONLY_UNFINISHED_KEY = "daily_only_unfinished"

    @staticmethod
    def reset_time(settings: dict | None = None) -> time:
        if settings is None:
            settings = SettingsStorage.load_settings()
        try:
            return datetime.strptime(settings.get(DailySettings.RESET_TIME_KEY, "00:00"), "%H:%M").time()
        except (TypeError, ValueError):
            return time()

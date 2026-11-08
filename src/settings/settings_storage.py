from typing import List
from src.app_data import get_data_file_path
from src.settings.setting import Setting
from src.json_file import StorageError, read_json, write_json


class SettingsStorage:
    """Handles loading and saving application settings to a JSON file."""

    FILENAME = "settings.json"

    @staticmethod
    def get_file_path() -> str:
        return get_data_file_path(SettingsStorage.FILENAME)

    @staticmethod
    def load_settings() -> dict:
        """
        Load all settings and return as a dictionary.
        """
        file_path = SettingsStorage.get_file_path()

        data = read_json(file_path, SettingsStorage._get_default_settings())
        if not isinstance(data, dict):
            raise StorageError(file_path, "read", "Expected a settings object")
        return data

    @staticmethod
    def load_settings_as_objects() -> List[Setting]:
        """
        Load all settings as Setting objects.
        """
        settings_dict = SettingsStorage.load_settings()
        return [Setting(key, value) for key, value in settings_dict.items()]

    @staticmethod
    def save_settings(settings_dict: dict) -> None:
        """
        Save settings from a dictionary.
        """
        file_path = SettingsStorage.get_file_path()

        write_json(file_path, settings_dict)

    @staticmethod
    def save_settings_from_objects(settings: List[Setting]) -> None:
        """
        Save settings from a list of Setting objects.
        """
        settings_dict = {setting.key: setting.value for setting in settings}
        SettingsStorage.save_settings(settings_dict)

    @staticmethod
    def _get_default_settings() -> dict:
        return {
            "startup": False,
            "theme": "Default",
        }

    @staticmethod
    def get_setting(key: str, default=None):
        """
        Get a single setting by key.
        """
        settings = SettingsStorage.load_settings()
        return settings.get(key, default)

    @staticmethod
    def set_setting(key: str, value) -> None:
        """
        Set a single setting by key.
        """
        settings = SettingsStorage.load_settings()
        settings[key] = value
        SettingsStorage.save_settings(settings)

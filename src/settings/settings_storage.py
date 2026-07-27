import json
import os
from typing import List
from src.app_data import get_data_file_path
from src.settings.setting import Setting


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

        if not os.path.exists(file_path):
            return SettingsStorage._get_default_settings()

        try:
            with open(file_path, "r") as f:
                data = json.load(f)
                return data
        except (json.JSONDecodeError, IOError):
            return SettingsStorage._get_default_settings()

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

        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w") as f:
                json.dump(settings_dict, f, indent=2)
        except IOError as e:
            print(f"Error saving settings: {e}")

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
            "launch_on_boot": False,
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

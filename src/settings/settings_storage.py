from src.app_data import get_data_file_path
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
    def save_settings(settings_dict: dict) -> None:
        """
        Save settings from a dictionary.
        """
        file_path = SettingsStorage.get_file_path()

        write_json(file_path, settings_dict)

    @staticmethod
    def _get_default_settings() -> dict:
        return {
            "startup": False,
            "theme": "Default",
        }

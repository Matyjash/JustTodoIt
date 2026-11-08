import sys
from PyQt5.QtWidgets import QApplication
from src.settings.theme import ThemeSettings
from src.task_file_storage import TaskFileStorage
from src.task_manager import TaskManager
from src.daily_task_reset import DailyTaskReset
from src.settings.daily import DailySettings
from src.json_file import StorageError
from src.ui.main_window import MainWindow
from src.ui.storage_error_handler import StorageErrorHandler


def main():
    app = QApplication(sys.argv)
    error_handler = StorageErrorHandler(app)
    sys.excepthook = error_handler
    try:
        task_file_storage = TaskFileStorage()
        try:
            window = MainWindow(
                task_manager=TaskManager(task_file_storage, DailyTaskReset(DailySettings.reset_time)),
                theme=ThemeSettings.load_selected_theme(),
            )
        except StorageError as error:
            error_handler.report(error)
            return 1
        window.display()
        return app.exec_()
    finally:
        sys.excepthook = error_handler.previous_hook


if __name__ == "__main__":
    sys.exit(main())

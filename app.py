import sys
from PyQt5.QtWidgets import QApplication
from src.settings.theme import ThemeSettings
from src.task_file_storage import TaskFileStorage
from src.task_manager import TaskManager
from src.daily_task_reset import DailyTaskReset
from src.settings.daily import DailySettings
from src.ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    task_file_storage = TaskFileStorage()
    window = MainWindow(
        task_manager=TaskManager(task_file_storage, DailyTaskReset(DailySettings.reset_time)),
        theme=ThemeSettings.load_selected_theme(),
    )
    window.display()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

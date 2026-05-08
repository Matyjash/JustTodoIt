import sys
from PyQt5.QtWidgets import QApplication
from src.task_file_storage import TaskFileStorage
from src.window import Window


def main():
    app = QApplication(sys.argv)

    task_file_storage = TaskFileStorage()
    window = Window(task_file_storage=task_file_storage)
    window.display()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

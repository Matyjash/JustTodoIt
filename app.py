import sys
from PyQt5.QtWidgets import QApplication
from src.task import Task
from src.window import Window


def main():
    app = QApplication(sys.argv)

    tasks = []

    window = Window(tasks=tasks)
    window.display()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

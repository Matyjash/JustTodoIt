import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMessageBox

from src.json_file import StorageError


class StorageErrorHandler:
    def __init__(self, app: QApplication):
        self.app = app
        self.failed = False
        self.previous_hook = sys.excepthook

    def __call__(self, error_type, error, traceback):
        if not isinstance(error, StorageError):
            self.previous_hook(error_type, error, traceback)
            return
        self.report(error)

    def report(self, error: StorageError) -> None:
        if self.failed:
            return
        self.failed = True
        for window in self.app.topLevelWidgets():
            for timer in window.findChildren(QTimer):
                timer.stop()
            window.setEnabled(False)
        message = QMessageBox()
        message.setIcon(QMessageBox.Critical)
        message.setWindowTitle("Storage error")
        message.setText("Your data could not be loaded or saved.")
        message.setInformativeText(
            "The app will close to avoid continuing with unsaved or incomplete data. "
            "The existing save file has not been replaced. "
            "Your latest change may not have been saved."
        )
        message.setDetailedText(str(error))
        message.exec_()
        self.app.exit(1)

from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtWidgets import QDialog


class WindowDrag:
    def __init__(self, window, threshold_y: int = 50):
        self.window = window
        self.threshold_y = threshold_y
        self.position = None

    def press(self, event: QEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.position = event.globalPos() - self.window.frameGeometry().topLeft()

    def move(self, event: QEvent) -> None:
        if event.buttons() == Qt.LeftButton and self.position is not None:
            if event.y() < self.threshold_y:
                self.window.move(event.globalPos() - self.position)

    def release(self, event: QEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.position = None


class DraggableDialog(QDialog):
    def __init__(self, parent=None, drag_threshold_y: int = 50):
        super().__init__(parent)
        self.window_drag = WindowDrag(self, drag_threshold_y)

    def mousePressEvent(self, event: QEvent) -> None:
        self.window_drag.press(event)

    def mouseMoveEvent(self, event: QEvent) -> None:
        self.window_drag.move(event)

    def mouseReleaseEvent(self, event: QEvent) -> None:
        self.window_drag.release(event)

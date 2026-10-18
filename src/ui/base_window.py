from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt, QEvent, QSettings
from src.ui.components.window_drag import WindowDrag


class Window(QMainWindow):
    """Base frameless window with title bar and dragging support."""

    def __init__(self, theme=None):
        """
        Initialize the Window.

        Args:
            theme: Theme configuration for the window (optional)
        """
        super().__init__()
        self.theme = theme
        self.window_drag = WindowDrag(self)
        self.mouse_press_x: int = 0
        self.mouse_press_y: int = 0
        self.is_maximized: bool = False
        self.normal_geometry = self.geometry()

    def init_window_base(self, window_title: str, window_x: int, window_y: int,
                         window_width: int, window_height: int) -> None:
        self.setWindowTitle(window_title)
        self.setGeometry(window_x, window_y, window_width, window_height)
        self.setWindowFlags(Qt.FramelessWindowHint)
        if self.theme:
            self.setStyleSheet(f"background-color: {self.theme.background_color};")

    def mousePressEvent(self, event: QEvent) -> None:
        self.window_drag.press(event)

    def mouseMoveEvent(self, event: QEvent) -> None:
        self.window_drag.move(event)

    def mouseReleaseEvent(self, event: QEvent) -> None:
        self.window_drag.release(event)

    def minimize_window(self) -> None:
        """Minimize the window."""
        self.showMinimized()

    def toggle_maximize(self) -> None:
        """Toggle between normal and maximized state."""
        if self.is_maximized:
            self.setGeometry(self.normal_geometry)
            self.maximize_btn.setText("□")
            self.is_maximized = False
        else:
            self.normal_geometry = self.geometry()
            self.setGeometry(self.screen().availableGeometry())
            self.maximize_btn.setText("▢")
            self.is_maximized = True

    def close_window(self) -> None:
        """Close the window."""
        self.close()

    def restore_geometry(self) -> None:
        """Restore window geometry from settings."""
        settings = QSettings("JustTodoIt", "JustTodoIt")
        geometry = settings.value("geometry", b"")
        window_state = settings.value("windowState", b"")

        if geometry:
            self.restoreGeometry(geometry)
        if window_state:
            self.restoreState(window_state)

    def closeEvent(self, event) -> None:
        """Save window geometry before closing."""
        settings = QSettings("JustTodoIt", "JustTodoIt")
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("windowState", self.saveState())
        event.accept()

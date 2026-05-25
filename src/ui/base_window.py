from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QEvent, QSettings
from PyQt5.QtGui import QFont

TITLE_BAR_HEIGHT = 30
CONTROL_BUTTON_SIZE = 24

TITLE_BAR_MARGIN_LEFT = 10
TITLE_BAR_MARGIN_TOP = 5
TITLE_BAR_MARGIN_RIGHT = 5
TITLE_BAR_MARGIN_BOTTOM = 5
TITLE_BAR_SPACING = 5
TITLE_BAR_BUTTON_PADDING = "4px"
TITLE_BAR_LABEL_PADDING = "5px"

DRAG_THRESHOLD_Y = 50

CONTROL_BUTTON_HOVER_ALPHA = 0.2
CONTROL_BUTTON_PRESSED_ALPHA = 0.3
CLOSE_BUTTON_HOVER_ALPHA = 0.3
CLOSE_BUTTON_PRESSED_ALPHA = 0.5


class Window(QMainWindow):
    """Base frameless window with title bar and dragging support."""

    def __init__(self, style=None):
        """
        Initialize the Window.

        Args:
            style: Style configuration for the window (optional)
        """
        super().__init__()
        self.style = style
        self.drag_position = None
        self.mouse_press_x: int = 0
        self.mouse_press_y: int = 0
        self.is_maximized: bool = False
        self.normal_geometry = self.geometry()

    def init_window_base(self, window_title: str, window_x: int, window_y: int,
                         window_width: int, window_height: int) -> None:
        self.setWindowTitle(window_title)
        self.setGeometry(window_x, window_y, window_width, window_height)
        self.setWindowFlags(Qt.FramelessWindowHint)
        if self.style:
            self.setStyleSheet(f"background-color: {self.style.window_background};")

    def create_title_bar(self, title_text: str) -> QHBoxLayout:
        title_bar_layout = QHBoxLayout()
        title_bar_layout.setContentsMargins(
            TITLE_BAR_MARGIN_LEFT,
            TITLE_BAR_MARGIN_TOP,
            TITLE_BAR_MARGIN_RIGHT,
            TITLE_BAR_MARGIN_BOTTOM,
        )
        title_bar_layout.setSpacing(TITLE_BAR_SPACING)

        title = QPushButton(title_text)
        if self.style:
            title.setFont(
                QFont(self.style.title_font_name, self.style.title_font_size, QFont.Bold)
            )
            title.setStyleSheet(
                f"QPushButton {{ background-color: transparent; color: {self.style.title_text_color}; "
                f"border: none; padding: {TITLE_BAR_LABEL_PADDING}; text-align: left; }}"
            )
        title.setEnabled(False)
        title_bar_layout.addWidget(title)

        title_bar_layout.addStretch()

        return title_bar_layout

    def add_minimize_button(self, title_bar_layout: QHBoxLayout) -> None:
        """Add minimize button to title bar."""
        minimize_btn = QPushButton("_")
        minimize_btn.setMaximumWidth(CONTROL_BUTTON_SIZE)
        if self.style:
            minimize_btn.setStyleSheet(
                f"QPushButton {{ background-color: transparent; color: {self.style.title_text_color}; border: none; "
                f"padding: {TITLE_BAR_BUTTON_PADDING}; font-weight: bold; }} "
                f"QPushButton:hover {{ background-color: rgba(0, 0, 0, {CONTROL_BUTTON_HOVER_ALPHA}); }} "
                f"QPushButton:pressed {{ background-color: rgba(0, 0, 0, {CONTROL_BUTTON_PRESSED_ALPHA}); }}"
            )
        minimize_btn.clicked.connect(self.minimize_window)
        title_bar_layout.addWidget(minimize_btn)

    def add_maximize_button(self, title_bar_layout: QHBoxLayout) -> QPushButton:
        """Add maximize button to title bar."""
        self.maximize_btn = QPushButton("□")
        self.maximize_btn.setMaximumWidth(CONTROL_BUTTON_SIZE)
        if self.style:
            self.maximize_btn.setStyleSheet(
                f"QPushButton {{ background-color: transparent; color: {self.style.title_text_color}; border: none; "
                f"padding: {TITLE_BAR_BUTTON_PADDING}; font-weight: bold; }} "
                f"QPushButton:hover {{ background-color: rgba(0, 0, 0, {CONTROL_BUTTON_HOVER_ALPHA}); }} "
                f"QPushButton:pressed {{ background-color: rgba(0, 0, 0, {CONTROL_BUTTON_PRESSED_ALPHA}); }}"
            )
        self.maximize_btn.clicked.connect(self.toggle_maximize)
        title_bar_layout.addWidget(self.maximize_btn)
        return self.maximize_btn

    def add_close_button(self, title_bar_layout: QHBoxLayout) -> None:
        """Add close button to title bar."""
        close_btn = QPushButton("✕")
        close_btn.setMaximumWidth(CONTROL_BUTTON_SIZE)
        if self.style:
            close_btn.setStyleSheet(
                f"QPushButton {{ background-color: transparent; color: {self.style.title_text_color}; border: none; "
                f"padding: {TITLE_BAR_BUTTON_PADDING}; font-weight: bold; }} "
                f"QPushButton:hover {{ background-color: rgba(255, 0, 0, {CLOSE_BUTTON_HOVER_ALPHA}); }} "
                f"QPushButton:pressed {{ background-color: rgba(255, 0, 0, {CLOSE_BUTTON_PRESSED_ALPHA}); }}"
            )
        close_btn.clicked.connect(self.close_window)
        title_bar_layout.addWidget(close_btn)

    def mousePressEvent(self, event: QEvent) -> None:
        """Handle mouse press for window dragging."""
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            self.mouse_press_x = event.x()
            self.mouse_press_y = event.y()

    def mouseMoveEvent(self, event: QEvent) -> None:
        """Handle mouse move for window dragging from title bar."""
        if event.buttons() == Qt.LeftButton and self.drag_position is not None:
            if event.y() < DRAG_THRESHOLD_Y:
                self.move(event.globalPos() - self.drag_position)

    def mouseReleaseEvent(self, event: QEvent) -> None:
        """Handle mouse release."""
        if event.button() == Qt.LeftButton:
            self.drag_position = None

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

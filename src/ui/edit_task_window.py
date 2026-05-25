from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QDialog,
)
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QFont
from typing import Optional
from src.task import Task
from src.ui.style import Style, DEFAULT_STYLE

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 150

CLOSE_BUTTON_TEXT = "✕"
DRAG_THRESHOLD_Y = 50
TITLE_BAR_HEIGHT = 30
CONTROL_BUTTON_SIZE = 24

TITLE_BAR_MARGIN_LEFT = 10
TITLE_BAR_MARGIN_TOP = 5
TITLE_BAR_MARGIN_RIGHT = 5
TITLE_BAR_MARGIN_BOTTOM = 5
TITLE_BAR_SPACING = 5
TITLE_BAR_BUTTON_PADDING = "4px"
TITLE_BAR_LABEL_PADDING = "5px"

CONTENT_MARGIN = 10
CONTENT_SPACING = 10

CONTROL_BUTTON_HOVER_ALPHA = 0.2
CONTROL_BUTTON_PRESSED_ALPHA = 0.3
CLOSE_BUTTON_HOVER_ALPHA = 0.3
CLOSE_BUTTON_PRESSED_ALPHA = 0.5


class EditTaskWindow(QDialog):
    """Dialog window for editing a task."""

    def __init__(
        self,
        task: Task,
        style: Style = DEFAULT_STYLE,
        start_reference_position: Optional[tuple] = None,
        parent=None,
    ):
        """
        Initialize the EditTaskWindow.

        Args:
            task: The Task object to edit
            style: Style configuration for the window (default: DEFAULT_STYLE)
            start_reference_position: Tuple of (x, y) coordinates for positioning (default: None)
            parent: Parent widget
        """
        super().__init__(parent)
        self.task = task
        self.style = style
        self.new_text: Optional[str] = None
        self.init_ui(start_reference_position)
        self.setWindowFlags(Qt.FramelessWindowHint)

    def init_ui(self, start_reference_position: Optional[tuple] = None) -> None:
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        if start_reference_position:
            x = (
                start_reference_position[0]
                + (start_reference_position[2] - WINDOW_WIDTH) // 2
            )
            y = (
                start_reference_position[1]
                + (start_reference_position[3] - WINDOW_HEIGHT) // 2
            )
            self.move(x, y)

        self.setStyleSheet(f"background-color: {self.style.window_background};")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addLayout(self._create_title_bar())

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(
            CONTENT_MARGIN, CONTENT_MARGIN, CONTENT_MARGIN, CONTENT_MARGIN
        )
        content_layout.setSpacing(CONTENT_SPACING)

        self.input_field = QLineEdit()
        self.input_field.setText(self.task.text)
        self.input_field.setStyleSheet(
            f"QLineEdit {{ padding: {self.style.input_padding}; border: {self.style.input_border}; border-radius: {self.style.input_border_radius}; }}"
        )
        content_layout.addWidget(self.input_field)

        button_layout = QHBoxLayout()
        button_layout.addStretch()

        save_button = QPushButton("Save")
        save_button.setStyleSheet(
            f"QPushButton {{ background-color: {self.style.save_btn_bg_color}; color: {self.style.save_btn_text_color}; "
            f"padding: {self.style.save_btn_padding}; border: none; border-radius: 4px; }}"
            f"QPushButton:hover {{ background-color: {self.style.save_btn_hover_color}; }}"
        )
        save_button.clicked.connect(self.save_task)
        button_layout.addWidget(save_button)

        content_layout.addLayout(button_layout)
        main_layout.addLayout(content_layout)

        self.setLayout(main_layout)
        self.drag_position: Optional[any] = None

    def _create_title_bar(self) -> QHBoxLayout:
        """Create the title bar with close button."""
        title_bar_widget = QWidget()
        title_bar_widget.setStyleSheet(
            f"background-color: {self.style.title_bg_color};"
        )
        title_bar_layout = QHBoxLayout()
        title_bar_layout.setContentsMargins(
            TITLE_BAR_MARGIN_LEFT,
            TITLE_BAR_MARGIN_TOP,
            TITLE_BAR_MARGIN_RIGHT,
            TITLE_BAR_MARGIN_BOTTOM,
        )
        title_bar_layout.setSpacing(TITLE_BAR_SPACING)

        title = QPushButton("Edit Task")
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

        close_btn = QPushButton(CLOSE_BUTTON_TEXT)
        close_btn.setMaximumWidth(CONTROL_BUTTON_SIZE)
        close_btn.setStyleSheet(
            f"QPushButton {{ background-color: transparent; color: {self.style.title_text_color}; border: none; "
            f"padding: {TITLE_BAR_BUTTON_PADDING}; font-weight: bold; }} "
            f"QPushButton:hover {{ background-color: rgba(255, 0, 0, {CLOSE_BUTTON_HOVER_ALPHA}); }} "
            f"QPushButton:pressed {{ background-color: rgba(255, 0, 0, {CLOSE_BUTTON_PRESSED_ALPHA}); }}"
        )
        close_btn.clicked.connect(self.cancel_edit)
        title_bar_layout.addWidget(close_btn)

        title_bar_widget.setLayout(title_bar_layout)

        title_bar_container = QHBoxLayout()
        title_bar_container.setContentsMargins(0, 0, 0, 0)
        title_bar_container.addWidget(title_bar_widget)
        return title_bar_container

    def save_task(self) -> None:
        self.new_text = self.input_field.text().strip()
        if self.new_text:
            self.accept()
        else:
            self.cancel_edit()

    def cancel_edit(self) -> None:
        self.new_text = None
        self.reject()

    def mousePressEvent(self, event: QEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event: QEvent) -> None:
        if event.buttons() == Qt.LeftButton and self.drag_position is not None:
            if event.y() < DRAG_THRESHOLD_Y:
                self.move(event.globalPos() - self.drag_position)

from PyQt5.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
)
from PyQt5.QtCore import Qt
from src.ui.components.title_bar import TitleBar
from src.ui.components.window_drag import DraggableDialog
from typing import Optional
from src.task import Task
from src.ui.theme.theme import DEFAULT_THEME, Theme

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 150

CONTENT_MARGIN = 10
CONTENT_SPACING = 10


class EditTaskDialog(DraggableDialog):
    """Dialog dialog for editing a task."""

    def __init__(
        self,
        task: Task,
        theme: Theme = DEFAULT_THEME,
        start_reference_position: Optional[tuple] = None,
        parent=None,
    ):
        """
        Initialize the EditTaskDialog.

        Args:
            task: The Task object to edit
            theme: Theme configuration for the dialog (default: DEFAULT_THEME)
            start_reference_position: Tuple of (x, y, width, height) for positioning (default: None)
            parent: Parent widget
        """
        super().__init__(parent)
        self.task = task
        self.theme = theme
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

        self.setStyleSheet(f"background-color: {self.theme.background_color};")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        title_bar = TitleBar("Edit Task", self.theme)
        title_bar.add_close_button(self.cancel_edit)
        main_layout.addWidget(title_bar)

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(CONTENT_MARGIN, CONTENT_MARGIN, CONTENT_MARGIN, CONTENT_MARGIN)
        content_layout.setSpacing(CONTENT_SPACING)

        self.input_field = QLineEdit()
        self.input_field.setText(self.task.text)
        self.input_field.setStyleSheet(
            f"QLineEdit {{ color: {self.theme.text_color}; padding: {self.theme.input_padding}; border: 1px solid {self.theme.border_color}; border-radius: {self.theme.input_border_radius}; }}"
            f"QLineEdit::placeholder {{ color: {self.theme.text_color}; }}"
        )
        content_layout.addWidget(self.input_field)

        button_layout = QHBoxLayout()
        button_layout.addStretch()

        save_button = QPushButton("Save")
        save_button.setStyleSheet(
            f"QPushButton {{ background-color: {self.theme.accept_color}; color: {self.theme.button_text_color}; "
            f"padding: {self.theme.save_btn_padding}; border: none; border-radius: 4px; }}"
        )
        save_button.clicked.connect(self.save_task)
        button_layout.addWidget(save_button)

        content_layout.addLayout(button_layout)
        main_layout.addLayout(content_layout)

        self.setLayout(main_layout)

    def save_task(self) -> None:
        self.new_text = self.input_field.text().strip()
        if self.new_text:
            self.accept()
        else:
            self.cancel_edit()

    def cancel_edit(self) -> None:
        self.new_text = None
        self.reject()

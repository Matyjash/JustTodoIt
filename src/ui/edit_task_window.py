from PyQt5.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QWidget,
    QLabel,
)
from PyQt5.QtCore import Qt, QSize, QTimer, pyqtSignal
from src.ui.components.title_bar import TitleBar
from src.ui.components.checkbox import ThemedCheckBox
from src.ui.components.window_drag import DraggableDialog
from typing import Optional
from src.task import Task
from src.task_uri import validate_uri
from src.ui.icons import create_icon
from src.ui.theme.theme import DEFAULT_THEME, Theme

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 220
URI_FEEDBACK_MS = 3000

CONTENT_MARGIN = 10
CONTENT_SPACING = 10


class EditTaskDialog(DraggableDialog):
    """Dialog dialog for editing a task."""

    uri_saved = pyqtSignal(str)

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
        self.saved_uri = task.uri
        self.uri_feedback_timer = QTimer(self)
        self.uri_feedback_timer.setSingleShot(True)
        self.uri_feedback_timer.timeout.connect(self._reset_uri_feedback)
        self.init_ui(start_reference_position)
        self.setWindowFlags(Qt.FramelessWindowHint)

    def init_ui(self, start_reference_position: Optional[tuple] = None) -> None:
        self.setMinimumWidth(WINDOW_WIDTH)
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
        main_layout.setAlignment(Qt.AlignTop)

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

        self.daily_checkbox = ThemedCheckBox(self.theme, "Daily ToDo")
        self.daily_checkbox.setChecked(self.task.daily)
        content_layout.addWidget(self.daily_checkbox)

        self.uri_checkbox = ThemedCheckBox(self.theme, "Enable quick access URI")
        self.uri_checkbox.setChecked(bool(self.saved_uri))
        content_layout.addWidget(self.uri_checkbox)

        self.uri_controls = QWidget()
        uri_layout = QVBoxLayout(self.uri_controls)
        uri_layout.setContentsMargins(0, 0, 0, 0)
        uri_layout.setSpacing(6)
        uri_row = QHBoxLayout()
        self.uri_input = QLineEdit(self.saved_uri)
        self.uri_input.setPlaceholderText("https://… or an application URI")
        self.uri_input.setAccessibleName("Quick access URI")
        self.uri_input.setStyleSheet(self.input_field.styleSheet())
        self.uri_input.textEdited.connect(self._reset_uri_feedback)
        self.uri_input.returnPressed.connect(self.save_uri)
        uri_row.addWidget(self.uri_input)
        self.uri_save_button = QPushButton()
        self.uri_save_button.setFixedSize(30, 30)
        self.uri_save_button.setIconSize(QSize(18, 18))
        self.uri_save_button.setAutoDefault(False)
        self.uri_save_button.setStyleSheet(
            f"QPushButton {{ background-color: {self.theme.neutral_color}; border: none; border-radius: 4px; }}"
        )
        self.uri_save_button.setToolTip("Save URI")
        self.uri_save_button.setAccessibleName("Save URI")
        self.uri_save_button.clicked.connect(self.save_uri)
        uri_row.addWidget(self.uri_save_button)
        uri_layout.addLayout(uri_row)
        self.uri_message = QLabel()
        self.uri_message.setWordWrap(True)
        uri_layout.addWidget(self.uri_message)
        content_layout.addWidget(self.uri_controls)
        self._reset_uri_feedback()
        self.uri_controls.setVisible(self.uri_checkbox.isChecked())
        self.uri_checkbox.toggled.connect(self._toggle_uri_controls)

        button_layout = QHBoxLayout()
        button_layout.addStretch()

        save_button = QPushButton("Save")
        save_button.setAutoDefault(False)
        save_button.setStyleSheet(
            f"QPushButton {{ background-color: {self.theme.accept_color}; color: {self.theme.button_text_color}; "
            f"padding: {self.theme.save_btn_padding}; border: none; border-radius: 4px; }}"
        )
        save_button.clicked.connect(self.save_task)
        button_layout.addWidget(save_button)

        content_layout.addLayout(button_layout)
        main_layout.addLayout(content_layout)

        self.setLayout(main_layout)

    def _toggle_uri_controls(self, enabled: bool) -> None:
        self._reset_uri_feedback()
        self.uri_controls.setVisible(enabled)
        self.adjustSize()
        if enabled:
            self.uri_input.setFocus()

    def _reset_uri_feedback(self) -> None:
        self.uri_feedback_timer.stop()
        self.uri_save_button.setIcon(create_icon("save", self.theme.button_text_color))
        self.uri_message.clear()
        self.uri_message.hide()
        if self.layout() is not None:
            self.adjustSize()

    def _show_uri_feedback(self, success: bool, message: str) -> None:
        color = self.theme.accept_color if success else self.theme.decline_color
        self.uri_save_button.setIcon(create_icon("check" if success else "cross", color))
        self.uri_message.setStyleSheet(f"color: {self.theme.text_color};")
        self.uri_message.setText(message)
        self.uri_message.show()
        self.adjustSize()
        self.uri_feedback_timer.start(URI_FEEDBACK_MS)

    def save_uri(self) -> None:
        try:
            uri = validate_uri(self.uri_input.text())
        except ValueError as error:
            self._show_uri_feedback(False, str(error))
            return
        self.uri_saved.emit(uri)
        self.saved_uri = uri
        self.uri_input.setText(uri)
        self._show_uri_feedback(True, "URI saved.")

    def save_task(self) -> None:
        if self.uri_checkbox.isChecked() and (
            not self.saved_uri or self.uri_input.text().strip() != self.saved_uri
        ):
            self._show_uri_feedback(False, "Save the URI using the button beside it first.")
            return
        self.new_text = self.input_field.text().strip()
        if self.new_text:
            self.accept()
        else:
            self.cancel_edit()

    def cancel_edit(self) -> None:
        self.new_text = None
        self.reject()

"""Main application window for the todo app."""

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QLineEdit,
    QPushButton,
    QDialog,
)
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QFont
from typing import Optional
from src.task import Task
from src.ui.style import Style, DEFAULT_STYLE
from src.ui.edit_task_window import EditTaskWindow
from src.ui.resizable_window import ResizableWindow

WINDOW_TITLE = "Todo App"
WINDOW_X = 100
WINDOW_Y = 100
WINDOW_WIDTH = 300
WINDOW_HEIGHT = 600
WINDOW_MARGIN = 10
WINDOW_SPACING = 10

TITLE_TEXT = "Just ToDo It"
INPUT_PLACEHOLDER = "Add a new task..."
ADD_BUTTON_TEXT = "Add"
DELETE_BUTTON_TEXT = "Delete Selected"
CLEAR_BUTTON_TEXT = "Clear All"

MINIMIZE_BUTTON_TEXT = "_"
MAXIMIZE_BUTTON_TEXT = "□"
RESTORE_BUTTON_TEXT = "▢"
CLOSE_BUTTON_TEXT = "✕"

CONTROL_BUTTON_HOVER_ALPHA = 0.2
CONTROL_BUTTON_PRESSED_ALPHA = 0.3
CLOSE_BUTTON_HOVER_ALPHA = 0.3
CLOSE_BUTTON_PRESSED_ALPHA = 0.5


class MainWindow(ResizableWindow):
    """Main window for the todo application."""

    def __init__(self, task_file_storage, style: Style = DEFAULT_STYLE):
        """
        Initialize the MainWindow.

        Args:
            task_file_storage: TaskFileStorage instance for persisting tasks
            style: Style configuration for the window (default: DEFAULT_STYLE)
        """
        super().__init__(style)
        self.task_file_storage = task_file_storage
        self.tasks = task_file_storage.load_tasks()
        self.init_ui()

    def init_ui(self) -> None:
        self.init_window_base(WINDOW_TITLE, WINDOW_X, WINDOW_Y, WINDOW_WIDTH, WINDOW_HEIGHT)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        top_layout = QVBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(0)

        # Create title bar widget
        title_bar_widget = QWidget()
        title_bar_widget.setStyleSheet(f"background-color: {self.style.title_bg_color};")
        
        # Create title bar layout and add buttons
        title_bar_layout = self.create_title_bar(TITLE_TEXT)
        self.add_minimize_button(title_bar_layout)
        self.add_maximize_button(title_bar_layout)
        self.add_close_button(title_bar_layout)
        
        title_bar_widget.setLayout(title_bar_layout)
        top_layout.addWidget(title_bar_widget)

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(WINDOW_MARGIN, WINDOW_MARGIN, WINDOW_MARGIN, WINDOW_MARGIN)
        self.main_layout.setSpacing(WINDOW_SPACING)

        self._init_input_layout()
        self._init_todo_list()
        self._init_button_layout()
        self.load_tasks()

        top_layout.addLayout(self.main_layout)
        central_widget.setLayout(top_layout)

        self.restore_geometry()

        self.restore_geometry()

    def _init_input_layout(self) -> None:
        input_layout = QHBoxLayout()

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText(INPUT_PLACEHOLDER)
        self.input_field.setStyleSheet(
            f"QLineEdit {{ padding: {self.style.input_padding}; border: {self.style.input_border}; border-radius: {self.style.input_border_radius}; }}"
        )
        self.input_field.returnPressed.connect(self.add_todo)

        add_button = QPushButton(ADD_BUTTON_TEXT)
        add_button.setStyleSheet(
            f"QPushButton {{ background-color: {self.style.add_btn_bg_color}; color: {self.style.add_btn_text_color}; "
            f"padding: {self.style.add_btn_padding}; border: none; border-radius: 4px; }}"
            f"QPushButton:hover {{ background-color: {self.style.add_btn_hover_color}; }}"
        )
        add_button.clicked.connect(self.add_todo)

        input_layout.addWidget(self.input_field)
        input_layout.addWidget(add_button)
        self.main_layout.addLayout(input_layout)

    def _init_todo_list(self) -> None:
        self.todo_list = QListWidget()
        self.todo_list.setStyleSheet(
            f"QListWidget {{ border: {self.style.list_border}; border-radius: {self.style.list_border_radius}; "
            f"background-color: {self.style.list_bg_color}; }}"
            f"QListWidget::item {{ padding: {self.style.list_item_padding}; border-bottom: {self.style.list_item_border_bottom}; }}"
            f"QListWidget::item:selected {{ background-color: {self.style.list_item_selected_bg}; }}"
        )
        self.main_layout.addWidget(self.todo_list)

    def _init_button_layout(self) -> None:
        button_layout = QHBoxLayout()

        delete_button = QPushButton(DELETE_BUTTON_TEXT)
        delete_button.setStyleSheet(
            f"QPushButton {{ background-color: {self.style.delete_btn_bg_color}; color: {self.style.delete_btn_text_color}; "
            f"padding: {self.style.delete_btn_padding}; border: none; border-radius: 4px; }}"
            f"QPushButton:hover {{ background-color: {self.style.delete_btn_hover_color}; }}"
        )
        delete_button.clicked.connect(self.delete_todo)

        clear_button = QPushButton(CLEAR_BUTTON_TEXT)
        clear_button.setStyleSheet(
            f"QPushButton {{ background-color: {self.style.clear_btn_bg_color}; color: {self.style.clear_btn_text_color}; "
            f"padding: {self.style.clear_btn_padding}; border: none; border-radius: 4px; }}"
            f"QPushButton:hover {{ background-color: {self.style.clear_btn_hover_color}; }}"
        )
        clear_button.clicked.connect(self.clear_all)

        button_layout.addWidget(delete_button)
        button_layout.addWidget(clear_button)
        self.main_layout.addLayout(button_layout)

    def load_tasks(self) -> None:
        self.todo_list.clear()
        for index, task in enumerate(self.tasks):
            item = QListWidgetItem()
            item.setData(Qt.UserRole, task)
            item.setFont(
                QFont(self.style.list_item_font_name, self.style.list_item_font_size)
            )
            self.todo_list.addItem(item)

            item_widget = QWidget()
            item_widget.setStyleSheet(f"background-color: {self.style.list_bg_color};")
            item_layout = QHBoxLayout()
            item_layout.setContentsMargins(0, 0, 0, 0)
            item_layout.setSpacing(5)

            task_label = QPushButton(str(task))
            task_label.setStyleSheet(
                f"QPushButton {{ background-color: transparent; color: black; border: none; text-align: left; padding: 0px; }}"
            )
            task_label.setEnabled(False)
            item_layout.addWidget(task_label)

            edit_button = QPushButton("E")
            edit_button.setMaximumWidth(30)
            edit_button.setStyleSheet(
                f"QPushButton {{ background-color: {self.style.edit_btn_bg_color}; color: {self.style.edit_btn_text_color}; "
                f"padding: {self.style.edit_btn_padding}; border: none; border-radius: 4px; }}"
                f"QPushButton:hover {{ background-color: {self.style.edit_btn_hover_color}; }}"
            )
            edit_button.clicked.connect(
                lambda checked, idx=index: self.open_edit_dialog(idx)
            )
            item_layout.addWidget(edit_button)

            item_widget.setLayout(item_layout)
            self.todo_list.setItemWidget(item, item_widget)

    def add_todo(self) -> None:
        text = self.input_field.text().strip()
        if not text:
            return

        task = Task(text=text, done=False)
        self.tasks.append(task)

        item = QListWidgetItem()
        item.setText(str(task))
        item.setData(Qt.UserRole, task)
        item.setFont(
            QFont(self.style.list_item_font_name, self.style.list_item_font_size)
        )
        self.todo_list.addItem(item)
        self.input_field.clear()
        self.task_file_storage.save_tasks(self.tasks)

    def delete_todo(self) -> None:
        row = self.todo_list.currentRow()
        if row >= 0:
            self.tasks.pop(row)
            self.todo_list.takeItem(row)
            self.task_file_storage.save_tasks(self.tasks)

    def open_edit_dialog(self, task_index: int) -> None:
        if task_index < 0 or task_index >= len(self.tasks):
            return

        task = self.tasks[task_index]
        main_geometry = self.frameGeometry()
        start_reference_position = (
            main_geometry.x(),
            main_geometry.y(),
            main_geometry.width(),
            main_geometry.height(),
        )
        edit_window = EditTaskWindow(task, self.style, start_reference_position)

        result = edit_window.exec_()

        if result == QDialog.Accepted and edit_window.new_text:
            task.text = edit_window.new_text
            self.task_file_storage.save_tasks(self.tasks)
            self.load_tasks()

    def clear_all(self) -> None:
        self.tasks.clear()
        self.todo_list.clear()
        self.task_file_storage.save_tasks(self.tasks)

    def mouseDoubleClickItem(self, item: QListWidgetItem) -> None:
        task = item.data(Qt.UserRole)
        if task:
            task.toggle()
            item.setText(str(task))
            self.task_file_storage.save_tasks(self.tasks)

    def mouseDoubleClickEvent(self, event: QEvent) -> None:
        item = self.todo_list.itemAt(
            self.todo_list.mapFromGlobal(self.mapToGlobal(event.pos()))
        )
        if item:
            self.mouseDoubleClickItem(item)

    def display(self) -> None:
        self.show()

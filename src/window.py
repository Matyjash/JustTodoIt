from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QLineEdit,
    QPushButton,
)
from PyQt5.QtCore import Qt, QEvent, QSettings
from PyQt5.QtGui import QFont
from typing import List, Optional
from src.task import Task
from src.style import Style, DEFAULT_STYLE

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

CONTROL_BUTTON_HOVER_ALPHA = 0.2
CONTROL_BUTTON_PRESSED_ALPHA = 0.3
CLOSE_BUTTON_HOVER_ALPHA = 0.3
CLOSE_BUTTON_PRESSED_ALPHA = 0.5


class Window(QMainWindow):
    """Main window for the todo application."""

    def __init__(self, tasks: List[Task], style: Style = DEFAULT_STYLE):
        """
        Initialize the Window.

        Args:
            tasks: List of Task objects to display
            style: Style configuration for the window (default: DEFAULT_STYLE)
        """
        super().__init__()
        self.tasks = tasks
        self.style = style
        self.init_ui()

    def init_ui(self) -> None:
        self._init_window()
        self._init_input_layout()
        self._init_todo_list()
        self._init_button_layout()
        self.load_tasks()
        self.drag_position: Optional[any] = None
        self.mouse_press_x: int = 0
        self.mouse_press_y: int = 0
        self.is_maximized: bool = False
        self.normal_geometry = self.geometry()
        self.restore_geometry()

    def _init_window(self) -> None:
        self.setWindowTitle(WINDOW_TITLE)
        self.setGeometry(WINDOW_X, WINDOW_Y, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(f"background-color: {self.style.window_background};")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        top_layout = QVBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(0)

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(
            WINDOW_MARGIN, WINDOW_MARGIN, WINDOW_MARGIN, WINDOW_MARGIN
        )
        self.main_layout.setSpacing(WINDOW_SPACING)

        top_layout.addLayout(self._create_title_bar())
        top_layout.addLayout(self.main_layout)
        central_widget.setLayout(top_layout)

    def _create_title_bar(self) -> QHBoxLayout:
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

        title = QPushButton(TITLE_TEXT)
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

        minimize_btn = QPushButton(MINIMIZE_BUTTON_TEXT)
        minimize_btn.setMaximumWidth(CONTROL_BUTTON_SIZE)
        minimize_btn.setStyleSheet(
            f"QPushButton {{ background-color: transparent; color: {self.style.title_text_color}; border: none; "
            f"padding: {TITLE_BAR_BUTTON_PADDING}; font-weight: bold; }} "
            f"QPushButton:hover {{ background-color: rgba(0, 0, 0, {CONTROL_BUTTON_HOVER_ALPHA}); }} "
            f"QPushButton:pressed {{ background-color: rgba(0, 0, 0, {CONTROL_BUTTON_PRESSED_ALPHA}); }}"
        )
        minimize_btn.clicked.connect(self.minimize_window)
        title_bar_layout.addWidget(minimize_btn)

        self.maximize_btn = QPushButton(MAXIMIZE_BUTTON_TEXT)
        self.maximize_btn.setMaximumWidth(CONTROL_BUTTON_SIZE)
        self.maximize_btn.setStyleSheet(
            f"QPushButton {{ background-color: transparent; color: {self.style.title_text_color}; border: none; "
            f"padding: {TITLE_BAR_BUTTON_PADDING}; font-weight: bold; }} "
            f"QPushButton:hover {{ background-color: rgba(0, 0, 0, {CONTROL_BUTTON_HOVER_ALPHA}); }} "
            f"QPushButton:pressed {{ background-color: rgba(0, 0, 0, {CONTROL_BUTTON_PRESSED_ALPHA}); }}"
        )
        self.maximize_btn.clicked.connect(self.toggle_maximize)
        title_bar_layout.addWidget(self.maximize_btn)

        close_btn = QPushButton(CLOSE_BUTTON_TEXT)
        close_btn.setMaximumWidth(CONTROL_BUTTON_SIZE)
        close_btn.setStyleSheet(
            f"QPushButton {{ background-color: transparent; color: {self.style.title_text_color}; border: none; "
            f"padding: {TITLE_BAR_BUTTON_PADDING}; font-weight: bold; }} "
            f"QPushButton:hover {{ background-color: rgba(255, 0, 0, {CLOSE_BUTTON_HOVER_ALPHA}); }} "
            f"QPushButton:pressed {{ background-color: rgba(255, 0, 0, {CLOSE_BUTTON_PRESSED_ALPHA}); }}"
        )
        close_btn.clicked.connect(self.close_window)
        title_bar_layout.addWidget(close_btn)

        title_bar_widget.setLayout(title_bar_layout)

        title_bar_container = QHBoxLayout()
        title_bar_container.setContentsMargins(0, 0, 0, 0)
        title_bar_container.addWidget(title_bar_widget)
        return title_bar_container

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
        for task in self.tasks:
            item = QListWidgetItem()
            item.setText(str(task))
            item.setData(Qt.UserRole, task)
            item.setFont(
                QFont(self.style.list_item_font_name, self.style.list_item_font_size)
            )
            self.todo_list.addItem(item)

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

    def delete_todo(self) -> None:
        row = self.todo_list.currentRow()
        if row >= 0:
            self.tasks.pop(row)
            self.todo_list.takeItem(row)

    def clear_all(self) -> None:
        self.tasks.clear()
        self.todo_list.clear()

    def mouseDoubleClickItem(self, item: QListWidgetItem) -> None:
        task = item.data(Qt.UserRole)
        if task:
            task.toggle()
            item.setText(str(task))

    def mousePressEvent(self, event: QEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            self.mouse_press_x = event.x()
            self.mouse_press_y = event.y()

    def mouseMoveEvent(self, event: QEvent) -> None:
        if event.buttons() == Qt.LeftButton and self.drag_position is not None:
            if event.y() < DRAG_THRESHOLD_Y:
                self.move(event.globalPos() - self.drag_position)

    def mouseDoubleClickEvent(self, event: QEvent) -> None:
        item = self.todo_list.itemAt(
            self.todo_list.mapFromGlobal(self.mapToGlobal(event.pos()))
        )
        if item:
            self.mouseDoubleClickItem(item)

    def minimize_window(self) -> None:
        self.showMinimized()

    def toggle_maximize(self) -> None:
        if self.is_maximized:
            self.setGeometry(self.normal_geometry)
            self.maximize_btn.setText(MAXIMIZE_BUTTON_TEXT)
            self.is_maximized = False
        else:
            self.normal_geometry = self.geometry()
            self.setGeometry(self.screen().availableGeometry())
            self.maximize_btn.setText(RESTORE_BUTTON_TEXT)
            self.is_maximized = True

    def close_window(self) -> None:
        self.close()

    def display(self) -> None:
        self.show()

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

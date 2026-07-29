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
    QAbstractItemView,
    QApplication,
)
from PyQt5.QtCore import Qt, QEvent, QSize
from PyQt5.QtGui import QFont
from typing import Optional
from src.task import Task
from src.ui.style import Style, DEFAULT_STYLE
from src.ui.edit_task_window import EditTaskDialog
from src.ui.settings_dialog import SettingsDialog
from src.ui.resizable_window import ResizableWindow

WINDOW_TITLE = "Todo App"
WINDOW_X = 100
WINDOW_Y = 100
WINDOW_WIDTH = 300
WINDOW_HEIGHT = 600
WINDOW_MARGIN = 10
WINDOW_SPACING = 10
TASK_ROW_HEIGHT = 36

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


class DraggableTodoList(QListWidget):
    """List widget that supports drag-and-drop reordering without losing rows."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self._dragged_row = -1

    def startDrag(self, supported_actions) -> None:
        self._dragged_row = self.currentRow()
        super().startDrag(supported_actions)

    def dropEvent(self, event):
        window = self.window()
        target_row = self.indexAt(event.pos()).row()

        if target_row < 0:
            target_row = self.count()
        elif event.pos().y() > self.visualItemRect(self.item(target_row)).center().y():
            target_row += 1

        if window is not None and hasattr(window, "_move_task_in_list"):
            window._move_task_in_list(self._dragged_row, target_row)

        self._dragged_row = -1
        event.acceptProposedAction()

    def start_drag_from_item(self, item: QListWidgetItem) -> None:
        """Start dragging a task when its custom row receives the gesture."""
        self.setCurrentItem(item)
        self.startDrag(Qt.MoveAction)


class DraggableTaskRow(QWidget):
    """A task row that forwards drag gestures from its child controls."""

    def __init__(self, todo_list: DraggableTodoList, item: QListWidgetItem):
        super().__init__()
        self.todo_list = todo_list
        self.item = item
        self.drag_start_position = None
        self.is_dragging = False

    def add_drag_source(self, widget: QWidget) -> None:
        """Allow a child widget to begin a list drag without disabling its click."""
        widget.installEventFilter(self)

    def eventFilter(self, watched, event):
        if self._handle_drag_event(event):
            return True
        return super().eventFilter(watched, event)

    def mousePressEvent(self, event) -> None:
        if not self._handle_drag_event(event):
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        if not self._handle_drag_event(event):
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        if not self._handle_drag_event(event):
            super().mouseReleaseEvent(event)

    def _handle_drag_event(self, event) -> bool:
        if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
            self.todo_list.setCurrentItem(self.item)
            self.drag_start_position = event.globalPos()
            self.is_dragging = False
        elif (
            event.type() == QEvent.MouseMove
            and event.buttons() & Qt.LeftButton
            and self.drag_start_position is not None
        ):
            distance = (event.globalPos() - self.drag_start_position).manhattanLength()
            if distance >= QApplication.startDragDistance():
                self.is_dragging = True
                self.todo_list.start_drag_from_item(self.item)
                return True
        elif event.type() == QEvent.MouseButtonRelease:
            should_consume_event = self.is_dragging
            self.drag_start_position = None
            self.is_dragging = False
            return should_consume_event

        return False


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
        self.init_window_base(
            WINDOW_TITLE, WINDOW_X, WINDOW_Y, WINDOW_WIDTH, WINDOW_HEIGHT
        )

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        top_layout = QVBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(0)

        title_bar_widget = QWidget()
        title_bar_widget.setStyleSheet(
            f"background-color: {self.style.title_bg_color};"
        )

        title_bar_layout = self.create_title_bar(TITLE_TEXT)

        #TODO: Replace with settings icon
        settings_button = QPushButton("⚙")
        settings_button.setMaximumWidth(35)
        settings_button.setStyleSheet(
            f"QPushButton {{ background-color: transparent; color: {self.style.title_text_color}; "
            f"border: none; font-size: 16px; padding: 0px; }}"
            f"QPushButton:hover {{ background-color: rgba(255, 255, 255, {CONTROL_BUTTON_HOVER_ALPHA}); }}"
            f"QPushButton:pressed {{ background-color: rgba(255, 255, 255, {CONTROL_BUTTON_PRESSED_ALPHA}); }}"
        )
        settings_button.clicked.connect(self.open_settings)
        title_bar_layout.addWidget(settings_button)

        self.add_minimize_button(title_bar_layout)
        self.add_maximize_button(title_bar_layout)
        self.add_close_button(title_bar_layout)

        title_bar_widget.setLayout(title_bar_layout)
        top_layout.addWidget(title_bar_widget)

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(
            WINDOW_MARGIN, WINDOW_MARGIN, WINDOW_MARGIN, WINDOW_MARGIN
        )
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
        self.todo_list = DraggableTodoList()
        self.todo_list.setStyleSheet(
            f"QListWidget {{ border: {self.style.list_border}; border-radius: {self.style.list_border_radius}; "
            f"background-color: {self.style.list_bg_color}; }}"
            f"QListWidget::item {{ border-bottom: {self.style.list_item_border_bottom}; }}"
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

    def _add_task_to_list(self, task: Task, task_index: int) -> None:
        item = QListWidgetItem()
        item.setData(Qt.UserRole, task)
        item.setFont(
            QFont(self.style.list_item_font_name, self.style.list_item_font_size)
        )
        item.setFlags(item.flags() | Qt.ItemIsDragEnabled)
        self.todo_list.addItem(item)

        item_widget = DraggableTaskRow(self.todo_list, item)
        item_widget.setStyleSheet(f"background-color: {self.style.list_bg_color};")
        item_layout = QHBoxLayout()
        item_layout.setContentsMargins(0, 0, 0, 0)
        item_layout.setSpacing(5)

        status_color = self.style.task_status_done_color if task.done else self.style.task_status_not_done_color
        status_square = QPushButton()
        status_square.setMaximumSize(self.style.task_status_square_size, self.style.task_status_square_size)
        status_square.setStyleSheet(
            f"QPushButton {{ background-color: {status_color}; border: none; border-radius: 2px; padding: {self.style.task_status_square_padding}; }}"
            f"QPushButton:hover {{ opacity: 0.8; }}"
        )
        status_square.clicked.connect(
            lambda checked, idx=task_index: self._toggle_task(idx)
        )
        item_widget.add_drag_source(status_square)
        item_layout.addWidget(status_square)

        task_label = QPushButton(task.text)
        task_label.setStyleSheet(
            f"QPushButton {{ background-color: transparent; color: black; border: none; text-align: left; padding: 0px; }}"
        )
        task_label.setEnabled(False)
        item_widget.add_drag_source(task_label)
        item_layout.addWidget(task_label)

        edit_button = QPushButton("E")
        edit_button.setMaximumWidth(30)
        edit_button.setStyleSheet(
            f"QPushButton {{ background-color: {self.style.edit_btn_bg_color}; color: {self.style.edit_btn_text_color}; "
            f"padding: {self.style.edit_btn_padding}; border: none; border-radius: 4px; }}"
            f"QPushButton:hover {{ background-color: {self.style.edit_btn_hover_color}; }}"
        )
        edit_button.clicked.connect(
            lambda checked, idx=task_index: self.open_edit_dialog(idx)
        )
        item_widget.add_drag_source(edit_button)
        item_layout.addWidget(edit_button)

        item_widget.setLayout(item_layout)
        item.setSizeHint(QSize(0, TASK_ROW_HEIGHT))
        self.todo_list.setItemWidget(item, item_widget)

    def load_tasks(self) -> None:
        """
        Load and display all tasks from storage.
        """
        self.tasks = sorted(self.tasks, key=lambda task: task.order)
        self.todo_list.clear()
        for index, task in enumerate(self.tasks):
            self._add_task_to_list(task, index)

    def add_todo(self) -> None:
        """
        Add a new task from the input field.
        """
        text = self.input_field.text().strip()
        if not text:
            return

        task = Task(text=text, done=False, order=len(self.tasks))
        self.tasks.append(task)

        task_index = len(self.tasks) - 1
        self.task_file_storage.save_tasks(self.tasks)
        self._add_task_to_list(task, task_index)
        self.input_field.clear()

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
        edit_dialog = EditTaskDialog(task, self.style, start_reference_position)

        result = edit_dialog.exec_()

        if result == QDialog.Accepted and edit_dialog.new_text:
            task.text = edit_dialog.new_text
            self.task_file_storage.save_tasks(self.tasks)
            self.load_tasks()

    def delete_todo(self) -> None:
        """
        Delete the selected task from the list and storage.
        """
        selected_items = self.todo_list.selectedItems()
        if not selected_items:
            return

        selected_tasks = [item.data(Qt.UserRole) for item in selected_items]
        for task in selected_tasks:
            if task in self.tasks:
                self.tasks.remove(task)

        self._normalize_task_orders()
        self.task_file_storage.save_tasks(self.tasks)
        self.load_tasks()

    def clear_all(self) -> None:
        self.tasks.clear()
        self.todo_list.clear()
        self.task_file_storage.save_tasks(self.tasks)

    def open_settings(self) -> None:
        """
        Open the settings dialog.
        """
        settings_dialog = SettingsDialog(self, self.style)
        settings_dialog.exec_()

    def _normalize_task_orders(self) -> None:
        for index, task in enumerate(self.tasks):
            task.order = index

    def _sync_tasks_from_list(self) -> None:
        reordered_tasks = []
        for row in range(self.todo_list.count()):
            item = self.todo_list.item(row)
            task = item.data(Qt.UserRole)
            if task is not None:
                reordered_tasks.append(task)

        self.tasks = reordered_tasks
        self._normalize_task_orders()
        self.task_file_storage.save_tasks(self.tasks)
        self.load_tasks()

    def _move_task_in_list(self, from_row: int, to_row: int) -> None:
        if from_row < 0 or from_row >= len(self.tasks):
            return

        task = self.tasks.pop(from_row)
        if to_row < 0:
            to_row = 0
        if to_row > len(self.tasks):
            to_row = len(self.tasks)
        if to_row > from_row:
            to_row = max(0, to_row - 1)
        self.tasks.insert(to_row, task)

        self._normalize_task_orders()
        self.task_file_storage.save_tasks(self.tasks)
        self.load_tasks()

    def _toggle_task(self, task_index: int) -> None:
        if task_index < 0 or task_index >= len(self.tasks):
            return
        self.tasks[task_index].toggle()
        self.task_file_storage.save_tasks(self.tasks)
        self.load_tasks()

    def display(self) -> None:
        self.show()

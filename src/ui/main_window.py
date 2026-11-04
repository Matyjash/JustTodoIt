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
    QLabel,
)
from PyQt5.QtCore import Qt, QEvent, QSize, QTimer
from PyQt5.QtGui import QFont
from src.settings.daily import DailySettings
from src.settings.settings_storage import SettingsStorage
from src.task import Task
from src.task_manager import TaskManager
from src.ui.theme.theme import DEFAULT_THEME, Theme
from src.ui.edit_task_window import EditTaskDialog
from src.ui.settings.settings_dialog import SettingsDialog
from src.ui.resizable_window import ResizableWindow
from src.ui.icons import create_icon
from src.ui.components.title_bar import TitleBar
from src.ui.components.checkbox import ThemedCheckBox

WINDOW_TITLE = "Todo App"
WINDOW_X = 100
WINDOW_Y = 100
WINDOW_WIDTH = 300
WINDOW_HEIGHT = 600
WINDOW_MARGIN = 10
WINDOW_SPACING = 10
TASK_ROW_HEIGHT = 36
ICON_BUTTON_SIZE = 30

TITLE_TEXT = "Just ToDo It"
INPUT_PLACEHOLDER = "Add a new task..."
ADD_BUTTON_TEXT = "Add"
DELETE_BUTTON_TEXT = "Delete Selected"

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

    def __init__(self, task_manager: TaskManager, theme: Theme = DEFAULT_THEME):
        super().__init__(theme)
        self.task_manager = task_manager
        self.init_ui()
        self.daily_timer = QTimer(self)
        self.daily_timer.timeout.connect(self._refresh_daily_tasks)
        self.daily_timer.start(1000)

    def init_ui(
        self, restore_geometry: bool = True, initialize_window: bool = True
    ) -> None:
        if initialize_window:
            self.init_window_base(
                WINDOW_TITLE, WINDOW_X, WINDOW_Y, WINDOW_WIDTH, WINDOW_HEIGHT
            )
        else:
            self.setStyleSheet(f"background-color: {self.theme.background_color};")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        top_layout = QVBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(0)

        title_bar = TitleBar(TITLE_TEXT, self.theme)

        settings_button = QPushButton()
        settings_button.setIcon(create_icon("settings", self.theme.button_text_color))
        settings_button.setIconSize(QSize(20, 20))
        settings_button.setToolTip("Settings")
        settings_button.setAccessibleName("Settings")
        settings_button.setMaximumWidth(35)
        settings_button.setStyleSheet(
            f"QPushButton {{ background-color: transparent; color: {self.theme.button_text_color}; "
            f"border: none; font-size: 16px; padding: 0px; }}"
            f"QPushButton:hover {{ background-color: rgba(255, 255, 255, {CONTROL_BUTTON_HOVER_ALPHA}); }}"
            f"QPushButton:pressed {{ background-color: rgba(255, 255, 255, {CONTROL_BUTTON_PRESSED_ALPHA}); }}"
        )
        settings_button.clicked.connect(self.open_settings)
        title_bar.add_widget(settings_button)

        title_bar.add_control_button("_", self.minimize_window)
        self.maximize_btn = title_bar.add_control_button("□", self.toggle_maximize)
        title_bar.add_close_button(self.close_window)
        top_layout.addWidget(title_bar)

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(
            WINDOW_MARGIN, WINDOW_MARGIN, WINDOW_MARGIN, WINDOW_MARGIN
        )
        self.main_layout.setSpacing(WINDOW_SPACING)

        self._init_input_layout()
        self._init_todo_list()
        self._init_button_layout()
        self._render_tasks()

        top_layout.addLayout(self.main_layout)
        central_widget.setLayout(top_layout)

        if restore_geometry:
            self.restore_geometry()

    def _init_input_layout(self) -> None:
        input_layout = QHBoxLayout()

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText(INPUT_PLACEHOLDER)
        self.input_field.setStyleSheet(
            f"QLineEdit {{ color: {self.theme.text_color}; padding: {self.theme.input_padding}; border: 1px solid {self.theme.border_color}; border-radius: {self.theme.input_border_radius}; }}"
            f"QLineEdit::placeholder {{ color: {self.theme.text_color}; }}"
        )
        self.input_field.returnPressed.connect(self.add_todo)

        add_button = QPushButton(ADD_BUTTON_TEXT)
        add_button.setStyleSheet(
            f"QPushButton {{ background-color: {self.theme.accept_color}; color: {self.theme.button_text_color}; "
            f"padding: {self.theme.add_btn_padding}; border: none; border-radius: 4px; }}"
        )
        add_button.clicked.connect(self.add_todo)

        input_layout.addWidget(self.input_field)
        input_layout.addWidget(add_button)
        self.main_layout.addLayout(input_layout)

    def _init_todo_list(self) -> None:
        self.todo_list = DraggableTodoList()
        self.todo_list.setStyleSheet(
            f"QListWidget {{ border: 1px solid {self.theme.border_color}; border-radius: {self.theme.list_border_radius}; "
            f"background-color: {self.theme.surface_color}; }}"
            f"QListWidget::item {{ border-bottom: 1px solid {self.theme.border_color}; }}"
            f"QListWidget::item:selected {{ background-color: {self.theme.background_color}; }}"
        )
        self.main_layout.addWidget(self.todo_list)

    def _init_button_layout(self) -> None:
        button_panel = QWidget()
        button_layout = QHBoxLayout(button_panel)
        button_layout.setContentsMargins(0, 0, 0, 0)

        self.delete_button = QPushButton(DELETE_BUTTON_TEXT)
        self.delete_button.setStyleSheet(
            f"QPushButton {{ background-color: {self.theme.decline_color}; color: {self.theme.button_text_color}; "
            f"padding: {self.theme.delete_btn_padding}; border: none; border-radius: 4px; }}"
        )
        button_panel.setFixedHeight(max(ICON_BUTTON_SIZE, self.delete_button.sizeHint().height()))
        self.delete_button.setText("")
        self.delete_button.setFixedSize(ICON_BUTTON_SIZE, ICON_BUTTON_SIZE)
        self.delete_button.setIcon(create_icon("delete", self.theme.button_text_color))
        self.delete_button.setIconSize(QSize(18, 18))
        self.delete_button.setToolTip(DELETE_BUTTON_TEXT)
        self.delete_button.setAccessibleName(DELETE_BUTTON_TEXT)
        self.delete_button.setStyleSheet(
            self.delete_button.styleSheet()
            + "QPushButton { padding: 0px; }"
            + f"QPushButton:disabled {{ background-color: {self.theme.neutral_color}; }}"
        )
        self.delete_button.clicked.connect(self.delete_todo)
        self.todo_list.itemSelectionChanged.connect(self._update_delete_button)
        self._update_delete_button()

        button_layout.addStretch()
        button_layout.addWidget(self.delete_button)
        self.main_layout.addWidget(button_panel)

    def _update_delete_button(self) -> None:
        self.delete_button.setEnabled(bool(self.todo_list.selectedItems()))

    def _add_task_to_list(self, task: Task) -> None:
        item = QListWidgetItem()
        item.setData(Qt.UserRole, task)
        item.setFont(
            QFont(self.theme.list_item_font_name, self.theme.list_item_font_size)
        )
        item.setFlags(item.flags() | Qt.ItemIsDragEnabled)
        self.todo_list.addItem(item)

        item_widget = DraggableTaskRow(self.todo_list, item)
        item_widget.setStyleSheet(f"background-color: {self.theme.surface_color};")
        item_layout = QHBoxLayout()
        status_inset = max(0, (TASK_ROW_HEIGHT - self.theme.task_status_square_size) // 2)
        item_layout.setContentsMargins(status_inset, 0, 0, 0)
        item_layout.setSpacing(status_inset)

        status_color = self.theme.accept_color if task.done else self.theme.neutral_color
        status_square = QPushButton()
        status_square.setMaximumSize(self.theme.task_status_square_size, self.theme.task_status_square_size)
        status_square.setStyleSheet(
            f"QPushButton {{ background-color: {status_color}; border: none; border-radius: 2px; padding: {self.theme.task_status_square_padding}; }}"
            f"QPushButton:hover {{ opacity: 0.8; }}"
        )
        status_square.clicked.connect(
            lambda checked, task=task: self._toggle_task(task)
        )
        item_widget.add_drag_source(status_square)
        item_layout.addWidget(status_square)

        task_label = QPushButton(task.text)
        task_label.setStyleSheet(
            f"QPushButton {{ background-color: transparent; color: {self.theme.text_color}; border: none; text-align: left; padding: 0px; }}"
        )
        task_label.setEnabled(False)
        item_widget.add_drag_source(task_label)
        item_layout.addWidget(task_label)

        edit_button = QPushButton()
        edit_button.setFixedSize(ICON_BUTTON_SIZE, ICON_BUTTON_SIZE)
        edit_button.setIcon(create_icon("edit", self.theme.button_text_color))
        edit_button.setIconSize(QSize(18, 18))
        edit_button.setToolTip("Edit task")
        edit_button.setAccessibleName("Edit task")
        edit_button.setStyleSheet(
            f"QPushButton {{ background-color: {self.theme.neutral_color}; color: {self.theme.button_text_color}; "
            f"padding: {self.theme.edit_btn_padding}; border: none; border-radius: 4px; }}"
        )
        edit_button.clicked.connect(
            lambda checked, task=task: self.open_edit_dialog(task)
        )
        item_widget.add_drag_source(edit_button)
        item_layout.addWidget(edit_button)

        item_widget.setLayout(item_layout)
        item.setSizeHint(QSize(0, TASK_ROW_HEIGHT))
        self.todo_list.setItemWidget(item, item_widget)

    def _render_tasks(self) -> None:
        selected = [item.data(Qt.UserRole) for item in self.todo_list.selectedItems()]
        self.todo_list.clear()
        tasks = self.task_manager.tasks
        self._render_daily_tasks(tasks)
        for task in tasks:
            if not task.daily:
                self._add_task_to_list(task)
        for row in range(self.todo_list.count()):
            item = self.todo_list.item(row)
            item.setSelected(item.data(Qt.UserRole) in selected)

    def _render_daily_tasks(self, tasks: tuple[Task, ...]) -> None:
        self.show_daily = None
        self.only_unfinished = None
        daily_tasks = [task for task in tasks if task.daily]
        if not daily_tasks:
            return
        self._add_daily_header()
        if self.show_daily.isChecked():
            for task in daily_tasks:
                if not self.only_unfinished.isChecked() or not task.done:
                    self._add_task_to_list(task)
        if any(not task.daily for task in tasks):
            self._add_daily_separator()

    def _add_daily_header(self) -> None:
        item = QListWidgetItem()
        item.setFlags(Qt.ItemIsEnabled)
        item.setSizeHint(QSize(0, 28))
        self.todo_list.addItem(item)
        header = QWidget()
        header.setStyleSheet(f"background-color: {self.theme.surface_color}; color: {self.theme.text_color};")
        layout = QHBoxLayout(header)
        layout.setContentsMargins(4, 0, 8, 0)
        label = QLabel("Daily")
        font = label.font()
        font.setBold(True)
        label.setFont(font)
        layout.addWidget(label)
        layout.addStretch()
        preferences = SettingsStorage.load_settings()
        self.show_daily = ThemedCheckBox(self.theme)
        self.only_unfinished = ThemedCheckBox(self.theme)
        self.show_daily.setChecked(preferences.get(DailySettings.SHOW_DAILY_KEY, True))
        self.only_unfinished.setChecked(preferences.get(DailySettings.ONLY_UNFINISHED_KEY, True))
        self.show_daily.setToolTip("Show daily ToDos")
        self.show_daily.setAccessibleName("Show daily ToDos")
        self.only_unfinished.setToolTip("Show only unfinished daily ToDos")
        self.only_unfinished.setAccessibleName("Show only unfinished daily ToDos")
        self.only_unfinished.setEnabled(self.show_daily.isChecked())
        for checkbox in (self.show_daily, self.only_unfinished):
            checkbox.toggled.connect(self._daily_visibility_changed)
            layout.addWidget(checkbox)
        self.todo_list.setItemWidget(item, header)

    def _add_daily_separator(self) -> None:
        item = QListWidgetItem()
        item.setFlags(Qt.NoItemFlags)
        item.setSizeHint(QSize(0, 2))
        self.todo_list.addItem(item)
        separator = QWidget()
        separator.setStyleSheet(f"background-color: {self.theme.lead_color};")
        self.todo_list.setItemWidget(item, separator)

    def _daily_visibility_changed(self) -> None:
        self.only_unfinished.setEnabled(self.show_daily.isChecked())
        settings = SettingsStorage.load_settings()
        settings[DailySettings.SHOW_DAILY_KEY] = self.show_daily.isChecked()
        settings[DailySettings.ONLY_UNFINISHED_KEY] = self.only_unfinished.isChecked()
        SettingsStorage.save_settings(settings)
        self._render_tasks()

    def _refresh_daily_tasks(self) -> None:
        if self.task_manager.reset_daily_tasks():
            self._render_tasks()

    def add_todo(self) -> None:
        """
        Add a new task from the input field.
        """
        task = self.task_manager.add(self.input_field.text())
        if task is None:
            return
        self._render_tasks()
        self.input_field.clear()

    def open_edit_dialog(self, task: Task) -> None:
        main_geometry = self.frameGeometry()
        start_reference_position = (
            main_geometry.x(),
            main_geometry.y(),
            main_geometry.width(),
            main_geometry.height(),
        )
        edit_dialog = EditTaskDialog(task, self.theme, start_reference_position)

        result = edit_dialog.exec_()

        if result == QDialog.Accepted and edit_dialog.new_text:
            self.task_manager.rename(task, edit_dialog.new_text)
            self.task_manager.set_daily(task, edit_dialog.daily_checkbox.isChecked())
            self._render_tasks()

    def delete_todo(self) -> None:
        """
        Delete the selected task from the list and storage.
        """
        selected_items = self.todo_list.selectedItems()
        if not selected_items:
            return

        selected_tasks = [item.data(Qt.UserRole) for item in selected_items]
        if self.task_manager.remove(selected_tasks):
            self._render_tasks()

    def open_settings(self) -> None:
        """
        Open the settings dialog.
        """
        settings_dialog = SettingsDialog(self, self.theme)
        settings_dialog.exec_()
        self._render_tasks()

    def set_theme(self, theme: Theme) -> None:
        """Reloads the window using the selected theme."""
        self.theme = theme
        self.init_ui(restore_geometry=False, initialize_window=False)

    def _move_task_in_list(self, from_row: int, to_row: int) -> None:
        source = self.todo_list.item(from_row)
        if source is None:
            return
        task = source.data(Qt.UserRole)
        if task is None:
            return
        before = None
        for row in range(max(0, to_row), self.todo_list.count()):
            candidate = self.todo_list.item(row).data(Qt.UserRole)
            if candidate is not None and candidate.daily == task.daily:
                before = candidate
                break
        if self.task_manager.move_visible(task, before):
            self._render_tasks()

    def _toggle_task(self, task: Task) -> None:
        if self.task_manager.toggle(task):
            self._render_tasks()

    def display(self) -> None:
        self.show()

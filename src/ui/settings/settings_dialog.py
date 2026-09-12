from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QPushButton, QVBoxLayout, QWidget
from src.settings.settings_storage import SettingsStorage
from src.ui.settings.sections.startup import Startup
from src.ui.settings.sections.theme import Theme as ThemeSection
from src.ui.theme.theme import DEFAULT_THEME, Theme


WINDOW_WIDTH = 400
WINDOW_HEIGHT = 250
DEFAULT_WINDOW_POSITION = 100

SETTINGS_TITLE = "Settings"
CLOSE_BUTTON_TEXT = "\u2715"
CLOSE_DIALOG_BUTTON_TEXT = "Close"
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
TITLE_BAR_DRAG_HEIGHT = 40

CLOSE_BUTTON_HOVER_ALPHA = 0.3
CLOSE_BUTTON_PRESSED_ALPHA = 0.5


class SettingsDialog(QDialog):
    """Displays and coordinates the available settings sections."""

    def __init__(self, parent=None, theme: Theme = DEFAULT_THEME):
        super().__init__(parent)
        self.theme = theme
        self.settings = SettingsStorage.load_settings()
        self.drag_position = None
        self.sections = [
            ThemeSection(self.settings, self.theme, self._apply_theme),
            Startup(self.settings, self.theme),
        ]
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self._init_ui()

    def _init_ui(self) -> None:
        self.setStyleSheet(f"background-color: {self.theme.background_color};")
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self._center_on_parent()

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addLayout(self._create_title_bar())
        main_layout.addLayout(self._create_content_layout())
        self.setLayout(main_layout)

    def _center_on_parent(self) -> None:
        if not self.parent():
            self.move(DEFAULT_WINDOW_POSITION, DEFAULT_WINDOW_POSITION)
            return

        parent_geometry = self.parent().frameGeometry()
        self.move(
            parent_geometry.x() + (parent_geometry.width() - WINDOW_WIDTH) // 2,
            parent_geometry.y() + (parent_geometry.height() - WINDOW_HEIGHT) // 2,
        )

    def _create_content_layout(self) -> QVBoxLayout:
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(
            CONTENT_MARGIN, CONTENT_MARGIN, CONTENT_MARGIN, CONTENT_MARGIN
        )
        content_layout.setSpacing(CONTENT_SPACING)

        for section in self.sections:
            if section.is_available():
                section.add_to_layout(content_layout)

        content_layout.addStretch()
        content_layout.addLayout(self._create_close_button_layout())
        return content_layout

    def _apply_theme(self, theme: Theme) -> None:
        parent = self.parent()
        if parent is not None and hasattr(parent, "set_theme"):
            parent.set_theme(theme)
        self.accept()

    def _create_title_bar(self) -> QHBoxLayout:
        title_bar_widget = QWidget()
        title_bar_widget.setStyleSheet(
            f"background-color: {self.theme.lead_color};"
        )

        title_bar_layout = QHBoxLayout()
        title_bar_layout.setContentsMargins(
            TITLE_BAR_MARGIN_LEFT,
            TITLE_BAR_MARGIN_TOP,
            TITLE_BAR_MARGIN_RIGHT,
            TITLE_BAR_MARGIN_BOTTOM,
        )
        title_bar_layout.setSpacing(TITLE_BAR_SPACING)
        title_bar_layout.addWidget(self._create_title_label())
        title_bar_layout.addStretch()
        title_bar_layout.addWidget(self._create_close_button())
        title_bar_widget.setLayout(title_bar_layout)

        title_bar_container = QHBoxLayout()
        title_bar_container.setContentsMargins(0, 0, 0, 0)
        title_bar_container.addWidget(title_bar_widget)
        return title_bar_container

    def _create_title_label(self) -> QPushButton:
        title = QPushButton(SETTINGS_TITLE)
        title.setFont(
            QFont(self.theme.title_font_name, self.theme.title_font_size, QFont.Bold)
        )
        title.setStyleSheet(
            "QPushButton { background-color: transparent; color: white; "
            f"border: none; padding: {TITLE_BAR_LABEL_PADDING}; text-align: left; }}"
        )
        title.setEnabled(False)
        return title

    def _create_close_button(self) -> QPushButton:
        close_button = QPushButton(CLOSE_BUTTON_TEXT)
        close_button.setMaximumWidth(CONTROL_BUTTON_SIZE)
        close_button.setStyleSheet(
            "QPushButton { background-color: transparent; color: white; border: none; "
            f"padding: {TITLE_BAR_BUTTON_PADDING}; font-weight: bold; }} "
            f"QPushButton:hover {{ background-color: rgba(255, 0, 0, {CLOSE_BUTTON_HOVER_ALPHA}); }} "
            f"QPushButton:pressed {{ background-color: rgba(255, 0, 0, {CLOSE_BUTTON_PRESSED_ALPHA}); }}"
        )
        close_button.clicked.connect(self.accept)
        return close_button

    def _create_close_button_layout(self) -> QHBoxLayout:
        button_layout = QHBoxLayout()
        close_button = QPushButton(CLOSE_DIALOG_BUTTON_TEXT)
        close_button.setStyleSheet(
            f"QPushButton {{ background-color: {self.theme.lead_color}; color: white; "
            f"padding: {self.theme.clear_btn_padding}; border: none; border-radius: 4px; }}"
        )
        close_button.clicked.connect(self.accept)
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        return button_layout

    def mousePressEvent(self, event: QEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event: QEvent) -> None:
        if event.buttons() == Qt.LeftButton and self.drag_position is not None:
            if event.y() < TITLE_BAR_DRAG_HEIGHT:
                self.move(event.globalPos() - self.drag_position)

    def mouseReleaseEvent(self, event: QEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.drag_position = None

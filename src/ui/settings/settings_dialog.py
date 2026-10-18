from PyQt5.QtCore import Qt
from src.ui.components.title_bar import TitleBar
from src.ui.components.window_drag import DraggableDialog
from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout
from src.settings.settings_storage import SettingsStorage
from src.ui.settings.sections.startup import Startup
from src.ui.settings.sections.theme import Theme as ThemeSection
from src.ui.theme.theme import DEFAULT_THEME, Theme


WINDOW_WIDTH = 400
WINDOW_HEIGHT = 250
DEFAULT_WINDOW_POSITION = 100

SETTINGS_TITLE = "Settings"
CLOSE_DIALOG_BUTTON_TEXT = "Close"
CONTENT_MARGIN = 10
CONTENT_SPACING = 10


class SettingsDialog(DraggableDialog):
    """Displays and coordinates the available settings sections."""

    def __init__(self, parent=None, theme: Theme = DEFAULT_THEME):
        super().__init__(parent, drag_threshold_y=40)
        self.theme = theme
        self.settings = SettingsStorage.load_settings()
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
        title_bar = TitleBar(SETTINGS_TITLE, self.theme)
        title_bar.add_close_button(self.accept)
        main_layout.addWidget(title_bar)
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

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from src.ui.components.title_bar import TitleBar
from src.ui.components.window_drag import DraggableDialog
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout
from src.settings.settings_storage import SettingsStorage
from src.ui.settings.sections.startup import Startup
from src.ui.settings.sections.daily import Daily
from src.ui.settings.sections.theme import Theme as ThemeSection
from src.ui.theme.theme import DEFAULT_THEME, Theme


WINDOW_WIDTH = 380
WINDOW_HEIGHT = 460
DEFAULT_WINDOW_POSITION = 100

SETTINGS_TITLE = "Settings"
CLOSE_DIALOG_BUTTON_TEXT = "Close"
CONTENT_MARGIN = 20
CONTENT_SPACING = 12


class SettingsDialog(DraggableDialog):
    """Displays and coordinates the available settings sections."""

    def __init__(self, parent=None, theme: Theme = DEFAULT_THEME):
        super().__init__(parent, drag_threshold_y=40)
        self.theme = theme
        self.settings = SettingsStorage.load_settings()
        self.sections = [
            ThemeSection(self.settings, self._apply_theme),
            Startup(self.settings, self.theme),
            Daily(self.settings),
        ]
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self._init_ui()

    def _init_ui(self) -> None:
        self.setWindowTitle(SETTINGS_TITLE)
        self.setObjectName("settingsDialog")
        self._apply_styles()
        self.setMinimumWidth(WINDOW_WIDTH)
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

    def _apply_styles(self) -> None:
        theme = self.theme
        muted = QColor(theme.text_color)
        surface = QColor(theme.surface_color)
        muted.setRgb(*[
            round(foreground * 0.65 + background * 0.35)
            for foreground, background in zip(muted.getRgb()[:3], surface.getRgb()[:3])
        ])
        self.setStyleSheet(
            f"QDialog#settingsDialog {{ background: {theme.background_color}; }}"
            f"QLabel, QCheckBox {{ color: {theme.text_color}; font-family: 'Segoe UI'; font-size: 10pt; background: transparent; }}"
            f"QFrame#settingsSection {{ background: {theme.surface_color}; border: 1px solid {theme.border_color}; border-radius: 8px; }}"
            "QLabel#sectionHeading { font-size: 10pt; font-weight: 600; }"
            f"QLabel#settingDescription, QLabel#saveHint {{ color: {muted.name()}; font-size: 9pt; }}"
            f"QComboBox, QTimeEdit {{ color: {theme.text_color}; background: {theme.background_color}; "
            f"border: 1px solid {theme.border_color}; border-radius: 5px; padding: 0 10px; font-family: 'Segoe UI'; font-size: 10pt; }}"
            f"QComboBox:focus, QTimeEdit:focus {{ border: 1px solid {theme.lead_color}; }}"
            f"QComboBox QAbstractItemView {{ color: {theme.text_color}; background: {theme.surface_color}; "
            f"selection-background-color: {theme.lead_color}; selection-color: {theme.button_text_color}; }}"
        )

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
        close_button.setMinimumSize(80, 34)
        close_button.setCursor(Qt.PointingHandCursor)
        close_button.setStyleSheet(
            f"QPushButton {{ background-color: {self.theme.lead_color}; color: {self.theme.button_text_color}; "
            "padding: 6px 16px; border: 1px solid transparent; border-radius: 5px; font-family: 'Segoe UI'; font-size: 10pt; }"
            f"QPushButton:hover, QPushButton:focus {{ border-color: {self.theme.text_color}; }}"
        )
        close_button.clicked.connect(self.accept)
        hint = QLabel("Changes save automatically")
        hint.setObjectName("saveHint")
        button_layout.addWidget(hint)
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        return button_layout

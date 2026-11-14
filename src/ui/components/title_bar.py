from collections.abc import Callable

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget

from src.ui.theme.theme import Theme


LAYOUT_MARGINS = (10, 5, 5, 5)
LAYOUT_SPACING = 5
LOGO_SIZE = 24
LOGO_DEVICE_PIXEL_RATIO = 2
LOGO_PIXMAP_SIZE = LOGO_SIZE * LOGO_DEVICE_PIXEL_RATIO
TITLE_PADDING = 5
CONTROL_BUTTON_MAX_WIDTH = 24
CONTROL_BUTTON_PADDING = 4
CONTROL_BUTTON_OVERLAY_RGB = "0, 0, 0"
CONTROL_BUTTON_HOVER_ALPHA = 0.2
CONTROL_BUTTON_PRESSED_ALPHA = 0.3
CLOSE_BUTTON_OVERLAY_RGB = "255, 0, 0"
CLOSE_BUTTON_HOVER_ALPHA = 0.3
CLOSE_BUTTON_PRESSED_ALPHA = 0.5


class TitleBar(QWidget):
    def __init__(self, title: str, theme: Theme | None, parent=None, *, icon: QIcon | None = None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.theme = theme
        if theme:
            self.setStyleSheet(f"background-color: {theme.lead_color};")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(*LAYOUT_MARGINS)
        layout.setSpacing(LAYOUT_SPACING)
        if icon is not None:
            logo = QLabel(self)
            logo.setFixedSize(LOGO_SIZE, LOGO_SIZE)
            pixmap = icon.pixmap(LOGO_PIXMAP_SIZE, LOGO_PIXMAP_SIZE)
            pixmap.setDevicePixelRatio(LOGO_DEVICE_PIXEL_RATIO)
            logo.setPixmap(pixmap)
            logo.setAttribute(Qt.WA_TransparentForMouseEvents, True)
            layout.addWidget(logo)
        label = QPushButton(title)
        if theme:
            label.setFont(QFont(theme.title_font_name, theme.title_font_size, QFont.Bold))
            label.setStyleSheet(
                f"QPushButton {{ background-color: transparent; color: {self.theme.button_text_color}; "
                f"border: none; padding: {TITLE_PADDING}px; text-align: left; }}"
            )
        label.setEnabled(False)
        label.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        layout.addWidget(label)
        layout.addStretch()

    def add_widget(self, widget: QWidget) -> None:
        self.layout().addWidget(widget)

    def add_control_button(
        self, text: str, action: Callable[[], None], *, close: bool = False
    ) -> QPushButton:
        button = QPushButton(text)
        button.setMaximumWidth(CONTROL_BUTTON_MAX_WIDTH)
        if self.theme:
            color = CLOSE_BUTTON_OVERLAY_RGB if close else CONTROL_BUTTON_OVERLAY_RGB
            hover_alpha = CLOSE_BUTTON_HOVER_ALPHA if close else CONTROL_BUTTON_HOVER_ALPHA
            pressed_alpha = CLOSE_BUTTON_PRESSED_ALPHA if close else CONTROL_BUTTON_PRESSED_ALPHA
            button.setStyleSheet(
                f"QPushButton {{ background-color: transparent; color: {self.theme.button_text_color}; border: none; "
                f"padding: {CONTROL_BUTTON_PADDING}px; font-weight: bold; }} "
                f"QPushButton:hover {{ background-color: rgba({color}, {hover_alpha}); }} "
                f"QPushButton:pressed {{ background-color: rgba({color}, {pressed_alpha}); }}"
            )
        button.clicked.connect(action)
        self.add_widget(button)
        return button

    def add_close_button(self, action: Callable[[], None]) -> QPushButton:
        return self.add_control_button("✕", action, close=True)

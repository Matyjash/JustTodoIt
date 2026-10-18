from collections.abc import Callable

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QWidget

from src.ui.theme.theme import Theme


class TitleBar(QWidget):
    def __init__(self, title: str, theme: Theme | None, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.theme = theme
        if theme:
            self.setStyleSheet(f"background-color: {theme.lead_color};")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 5, 5)
        layout.setSpacing(5)
        label = QPushButton(title)
        if theme:
            label.setFont(QFont(theme.title_font_name, theme.title_font_size, QFont.Bold))
            label.setStyleSheet(
                "QPushButton { background-color: transparent; color: white; "
                "border: none; padding: 5px; text-align: left; }"
            )
        label.setEnabled(False)
        layout.addWidget(label)
        layout.addStretch()

    def add_widget(self, widget: QWidget) -> None:
        self.layout().addWidget(widget)

    def add_control_button(
        self, text: str, action: Callable[[], None], *, close: bool = False
    ) -> QPushButton:
        button = QPushButton(text)
        button.setMaximumWidth(24)
        if self.theme:
            color = "255, 0, 0" if close else "0, 0, 0"
            hover_alpha, pressed_alpha = (0.3, 0.5) if close else (0.2, 0.3)
            button.setStyleSheet(
                "QPushButton { background-color: transparent; color: white; border: none; "
                "padding: 4px; font-weight: bold; } "
                f"QPushButton:hover {{ background-color: rgba({color}, {hover_alpha}); }} "
                f"QPushButton:pressed {{ background-color: rgba({color}, {pressed_alpha}); }}"
            )
        button.clicked.connect(action)
        self.add_widget(button)
        return button

    def add_close_button(self, action: Callable[[], None]) -> QPushButton:
        return self.add_control_button("✕", action, close=True)

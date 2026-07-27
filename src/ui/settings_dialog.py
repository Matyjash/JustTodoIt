from PyQt5.QtWidgets import (
    QDialog,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QCheckBox,
    QPushButton,
    QLabel,
)
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QFont
from src.ui.style import Style, DEFAULT_STYLE
from src.settings.settings_storage import SettingsStorage
import platform
import sys

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 250

CLOSE_BUTTON_TEXT = "✕"
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

LAYOUT_SPACING = 15
LAYOUT_MARGIN = 20

INFO_LABEL_FONT_SIZE = "9pt"
INFO_LABEL_TEXT_COLOR = "gray"

CLOSE_DIALOG_BUTTON_TEXT = "Close"

CONTROL_BUTTON_HOVER_ALPHA = 0.2
CONTROL_BUTTON_PRESSED_ALPHA = 0.3
CLOSE_BUTTON_HOVER_ALPHA = 0.3
CLOSE_BUTTON_PRESSED_ALPHA = 0.5


class SettingsDialog(QDialog):
    """Dialog for application settings."""

    def __init__(self, parent=None, style: Style = DEFAULT_STYLE):
        """
        Initialize the SettingsDialog.

        Args:
            parent: Parent widget
            style: Style configuration for the dialog (default: DEFAULT_STYLE)
        """
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.style = style
        self.settings = SettingsStorage.load_settings()
        self.drag_position = None
        self.init_ui()

    def init_ui(self) -> None:
        """
        Initialize the UI components.
        """
        self.setStyleSheet(f"background-color: {self.style.window_background};")
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        if self.parent():
            parent_geometry = self.parent().frameGeometry()
            center_x = (
                parent_geometry.x() + (parent_geometry.width() - WINDOW_WIDTH) // 2
            )
            center_y = (
                parent_geometry.y() + (parent_geometry.height() - WINDOW_HEIGHT) // 2
            )
            self.move(center_x, center_y)
        else:
            self.move(100, 100)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addLayout(self._create_title_bar())

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(
            CONTENT_MARGIN, CONTENT_MARGIN, CONTENT_MARGIN, CONTENT_MARGIN
        )
        content_layout.setSpacing(CONTENT_SPACING)

        if self._is_boot_launch_supported():
            boot_label = QLabel("Launch on system boot:")
            content_layout.addWidget(boot_label)

            self.boot_checkbox = QCheckBox("Enable")
            self.boot_checkbox.setChecked(self.settings.get("launch_on_boot", False))
            self.boot_checkbox.stateChanged.connect(self.on_boot_checkbox_changed)
            content_layout.addWidget(self.boot_checkbox)

        if platform.system() == "Windows":
            info_label = QLabel(
                "Note: Admin privileges may be required to enable this feature."
            )
            info_label.setStyleSheet(
                f"color: {INFO_LABEL_TEXT_COLOR}; font-size: {INFO_LABEL_FONT_SIZE};"
            )
            content_layout.addWidget(info_label)

        content_layout.addStretch()

        button_layout = QHBoxLayout()

        close_button = QPushButton(CLOSE_DIALOG_BUTTON_TEXT)
        close_button.setStyleSheet(
            f"QPushButton {{ background-color: {self.style.clear_btn_bg_color}; color: {self.style.clear_btn_text_color}; "
            f"padding: {self.style.clear_btn_padding}; border: none; border-radius: 4px; }}"
            f"QPushButton:hover {{ background-color: {self.style.clear_btn_hover_color}; }}"
        )
        close_button.clicked.connect(self.accept)

        button_layout.addStretch()
        button_layout.addWidget(close_button)
        content_layout.addLayout(button_layout)

        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

    @staticmethod
    def _is_boot_launch_supported() -> bool:
        """Return whether this installation can register itself for Windows startup."""
        return platform.system() == "Windows" and getattr(sys, "frozen", False)

    def on_boot_checkbox_changed(self) -> None:
        """
        Handle boot checkbox state change.
        """
        if not self._is_boot_launch_supported():
            return

        is_checked = self.boot_checkbox.isChecked()
        self.settings["launch_on_boot"] = is_checked
        SettingsStorage.save_settings(self.settings)

        if is_checked:
            self.enable_launch_on_boot()
        else:
            self.disable_launch_on_boot()

    def _create_title_bar(self) -> QHBoxLayout:
        """
        Create the title bar with close button.
        """
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

        title = QPushButton("Settings")
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

        close_btn = QPushButton(CLOSE_BUTTON_TEXT)
        close_btn.setMaximumWidth(CONTROL_BUTTON_SIZE)
        close_btn.setStyleSheet(
            f"QPushButton {{ background-color: transparent; color: {self.style.title_text_color}; border: none; "
            f"padding: {TITLE_BAR_BUTTON_PADDING}; font-weight: bold; }} "
            f"QPushButton:hover {{ background-color: rgba(255, 0, 0, {CLOSE_BUTTON_HOVER_ALPHA}); }} "
            f"QPushButton:pressed {{ background-color: rgba(255, 0, 0, {CLOSE_BUTTON_PRESSED_ALPHA}); }}"
        )
        close_btn.clicked.connect(self.accept)
        title_bar_layout.addWidget(close_btn)

        title_bar_widget.setLayout(title_bar_layout)

        title_bar_container = QHBoxLayout()
        title_bar_container.setContentsMargins(0, 0, 0, 0)
        title_bar_container.addWidget(title_bar_widget)
        return title_bar_container

    def enable_launch_on_boot(self) -> None:
        """
        Enable launching the app on system boot.
        """
        system = platform.system()

        if system == "Windows":
            self._enable_boot_windows()
        elif system == "Darwin":
            self._enable_boot_macos()
        elif system == "Linux":
            self._enable_boot_linux()

    def disable_launch_on_boot(self) -> None:
        """
        Disable launching the app on system boot.
        """
        system = platform.system()

        if system == "Windows":
            self._disable_boot_windows()
        elif system == "Darwin":
            self._disable_boot_macos()
        elif system == "Linux":
            self._disable_boot_linux()

    def _enable_boot_windows(self) -> None:
        """
        Add app to Windows startup.
        """
        import winreg

        try:
            executable_path = f'"{sys.executable}"'
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_SET_VALUE,
            ) as key:
                winreg.SetValueEx(
                    key, "JustTodoIt", 0, winreg.REG_SZ, executable_path
                )
        except OSError as error:
            print(f"Error enabling boot startup: {error}")

    def _disable_boot_windows(self) -> None:
        """
        Remove app from Windows startup.
        """
        import winreg

        try:
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_SET_VALUE,
            ) as key:
                winreg.DeleteValue(key, "JustTodoIt")
        except OSError as error:
            print(f"Error disabling boot startup: {error}")

    def _enable_boot_macos(self) -> None:
        """
        Add app to macOS startup.
        """
        print("macOS boot startup not yet implemented")

    def _disable_boot_macos(self) -> None:
        """
        Remove app from macOS startup.
        """
        print("macOS boot startup not yet implemented")

    def _enable_boot_linux(self) -> None:
        """
        Add app to Linux startup.
        """
        print("Linux boot startup not yet implemented")

    def _disable_boot_linux(self) -> None:
        """
        Remove app from Linux startup.
        """
        print("Linux boot startup not yet implemented")

    def mousePressEvent(self, event: QEvent) -> None:
        """
        Handle mouse press for title bar dragging.
        """
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event: QEvent) -> None:
        """
        Handle mouse move for title bar dragging.
        """
        if event.buttons() == Qt.LeftButton and self.drag_position is not None:
            if event.y() < 40:
                self.move(event.globalPos() - self.drag_position)

    def mouseReleaseEvent(self, event: QEvent) -> None:
        """
        Handle mouse release.
        """
        if event.button() == Qt.LeftButton:
            self.drag_position = None

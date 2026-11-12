from abc import ABC, abstractmethod
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout


class Setting(ABC):
    """Defines the interface for a settings dialog section."""

    def create_section(self, layout, title: str) -> QVBoxLayout:
        card = QFrame()
        card.setObjectName("settingsSection")
        content = QVBoxLayout(card)
        content.setContentsMargins(16, 14, 16, 14)
        content.setSpacing(10)
        heading = QLabel(title)
        heading.setObjectName("sectionHeading")
        content.addWidget(heading)
        layout.addWidget(card)
        return content

    def add_control(self, layout, text: str, control) -> None:
        row = QHBoxLayout()
        label = QLabel(text)
        label.setBuddy(control)
        row.addWidget(label)
        row.addStretch()
        control.setMinimumWidth(144)
        control.setMinimumHeight(34)
        row.addWidget(control)
        layout.addLayout(row)

    def add_description(self, layout, text: str) -> None:
        label = QLabel(text)
        label.setObjectName("settingDescription")
        label.setWordWrap(True)
        layout.addWidget(label)

    @abstractmethod
    def is_available(self) -> bool:
        pass

    @abstractmethod
    def add_to_layout(self, layout) -> None:
        pass

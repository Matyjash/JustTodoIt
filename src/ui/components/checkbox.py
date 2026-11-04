from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QColor, QPainter, QPainterPath, QPen
from PyQt5.QtWidgets import QCheckBox, QStyle, QStyleOptionButton

from src.ui.theme.theme import Theme


class ThemedCheckBox(QCheckBox):
    """Checkbox with a scalable, theme-colored square and checkmark."""

    def __init__(self, theme: Theme, text: str = "", parent=None):
        super().__init__(text, parent)
        self.theme = theme
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(
            f"QCheckBox {{ color: {theme.text_color}; spacing: 6px; }}"
            f"QCheckBox:disabled {{ color: {theme.neutral_color}; }}"
            "QCheckBox::indicator { width: 18px; height: 18px; "
            "background: transparent; border: none; image: none; }"
        )

    def paintEvent(self, event) -> None:
        super().paintEvent(event)
        option = QStyleOptionButton()
        self.initStyleOption(option)
        indicator = self.style().subElementRect(QStyle.SE_CheckBoxIndicator, option, self)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        if not self.isEnabled():
            painter.setOpacity(0.45)
        checked = self.checkState() != Qt.Unchecked
        highlighted = self.isEnabled() and bool(option.state & (QStyle.State_MouseOver | QStyle.State_HasFocus))
        fill = self.theme.lead_color if checked else self.theme.surface_color
        border = self.theme.lead_color if checked or highlighted else self.theme.neutral_color
        square = QRectF(indicator).adjusted(2, 2, -2, -2)
        painter.setBrush(QColor(fill))
        painter.setPen(QPen(QColor(border), 1.5))
        painter.drawRoundedRect(square, 2, 2)
        if highlighted:
            painter.setBrush(Qt.NoBrush)
            painter.setPen(QPen(QColor(self.theme.lead_color), 1))
            painter.drawRoundedRect(QRectF(indicator).adjusted(0.5, 0.5, -0.5, -0.5), 3, 3)
        if checked:
            painter.setPen(QPen(QColor(self.theme.button_text_color), 1.8, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            mark = QPainterPath()
            if self.checkState() == Qt.PartiallyChecked:
                mark.moveTo(square.left() + 3, square.center().y())
                mark.lineTo(square.right() - 3, square.center().y())
            else:
                mark.moveTo(square.left() + 3, square.center().y())
                mark.lineTo(square.left() + 6, square.bottom() - 4)
                mark.lineTo(square.right() - 2.5, square.top() + 4)
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(mark)
        painter.end()

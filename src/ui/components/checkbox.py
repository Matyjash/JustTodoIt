from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QColor, QIcon, QPainter, QPainterPath, QPen
from PyQt5.QtWidgets import QCheckBox, QStyle, QStyleOptionButton

from src.ui.theme.theme import Theme


DISABLED_OPACITY = 0.45
BORDER_WIDTH = 1.5
CHECKMARK_WIDTH = 1.8


class ThemedCheckBox(QCheckBox):
    """Checkbox with a scalable, theme-colored square and checkmark."""

    def __init__(self, theme: Theme, text: str = "", parent=None, indicator_icon: QIcon | None = None):
        super().__init__(text, parent)
        self.theme = theme
        self.indicator_icon = indicator_icon
        indicator_size = 24 if indicator_icon is not None else 18
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(
            f"QCheckBox {{ color: {theme.text_color}; spacing: 6px; }}"
            f"QCheckBox:disabled {{ color: {theme.neutral_color}; }}"
            f"QCheckBox::indicator {{ width: {indicator_size}px; height: {indicator_size}px; "
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
            painter.setOpacity(DISABLED_OPACITY)
        checked = self.checkState() != Qt.Unchecked
        highlighted = self.isEnabled() and bool(option.state & (QStyle.State_MouseOver | QStyle.State_HasFocus))
        fill = self.theme.lead_color if checked else self.theme.surface_color
        border = self.theme.lead_color if checked or highlighted else self.theme.neutral_color
        if self.indicator_icon is not None:
            border = self.theme.neutral_color
        square = QRectF(indicator).adjusted(2, 2, -2, -2)
        painter.setBrush(QColor(fill))
        painter.setPen(QPen(QColor(border), BORDER_WIDTH))
        painter.drawRoundedRect(square, 2, 2)
        if highlighted:
            painter.setBrush(Qt.NoBrush)
            painter.setPen(QPen(QColor(self.theme.lead_color), 1))
            painter.drawRoundedRect(QRectF(indicator).adjusted(0.5, 0.5, -0.5, -0.5), 3, 3)
        if self.indicator_icon is not None:
            self.indicator_icon.paint(painter, indicator.adjusted(4, 4, -4, -4), Qt.AlignCenter, QIcon.Normal)
        elif checked:
            painter.setPen(QPen(QColor(self.theme.button_text_color), CHECKMARK_WIDTH, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
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

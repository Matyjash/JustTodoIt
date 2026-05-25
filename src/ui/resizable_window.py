from PyQt5.QtCore import Qt, QEvent
from src.ui.base_window import Window

RESIZE_THRESHOLD = 10
MIN_WIDTH = 200
MIN_HEIGHT = 300


class ResizableWindow(Window):
    """Window that can be resized by dragging edges and corners."""

    def __init__(self, style=None):
        """
        Initialize the ResizableWindow.

        Args:
            style: Style configuration for the window (optional)
        """
        super().__init__(style)
        self.is_resizing: bool = False
        self.resize_direction: str = ""
        self.last_mouse_x: int = 0
        self.last_mouse_y: int = 0

    def _get_resize_direction(self, x: int, y: int) -> str:
        """
        Determine which edge/corner the cursor is near.

        Args:
            x: X coordinate relative to window
            y: Y coordinate relative to window

        Returns:
            String indicating resize direction: "top-left", "left", etc., or empty string
        """
        rect = self.rect()
        width = rect.width()
        height = rect.height()
        threshold = RESIZE_THRESHOLD

        near_left = x < threshold
        near_right = x > width - threshold
        near_top = y < threshold
        near_bottom = y > height - threshold

        if near_top and near_left:
            return "top-left"
        if near_top and near_right:
            return "top-right"
        if near_bottom and near_left:
            return "bottom-left"
        if near_bottom and near_right:
            return "bottom-right"

        if near_left:
            return "left"
        if near_right:
            return "right"
        if near_top:
            return "top"
        if near_bottom:
            return "bottom"

        return ""

    def _get_cursor_for_direction(self, direction: str):
        """
        Get the appropriate cursor for a resize direction.

        Args:
            direction: Resize direction string

        Returns:
            Qt cursor type or None if no resize direction
        """
        cursor_map = {
            "top-left": Qt.SizeFDiagCursor,
            "top-right": Qt.SizeBDiagCursor,
            "bottom-left": Qt.SizeBDiagCursor,
            "bottom-right": Qt.SizeFDiagCursor,
            "left": Qt.SizeHorCursor,
            "right": Qt.SizeHorCursor,
            "top": Qt.SizeVerCursor,
            "bottom": Qt.SizeVerCursor,
        }

        return cursor_map.get(direction)

    def _calculate_new_geometry(self, global_pos_x: int, global_pos_y: int) -> tuple:
        """
        Calculate new geometry based on resize direction.

        Args:
            global_pos_x: Current global X position of mouse
            global_pos_y: Current global Y position of mouse

        Returns:
            Tuple of (new_x, new_y, new_width, new_height)
        """
        geometry = self.frameGeometry()
        x, y, width, height = (
            geometry.x(),
            geometry.y(),
            geometry.width(),
            geometry.height(),
        )
        direction = self.resize_direction

        new_x = x
        new_y = y
        new_width = width
        new_height = height

        delta_x = global_pos_x - x - self.last_mouse_x
        delta_y = global_pos_y - y - self.last_mouse_y

        if "left" in direction:
            delta = global_pos_x - x
            new_width = max(MIN_WIDTH, width - delta)
            new_x = x + (width - new_width)

        if "right" in direction:
            new_width = max(MIN_WIDTH, width + delta_x)

        if "top" in direction:
            delta = global_pos_y - y
            new_height = max(MIN_HEIGHT, height - delta)
            new_y = y + (height - new_height)

        if "bottom" in direction:
            new_height = max(MIN_HEIGHT, height + delta_y)

        return (new_x, new_y, new_width, new_height)

    def mousePressEvent(self, event: QEvent) -> None:
        """Handle mouse press for resizing and dragging."""
        if event.button() == Qt.LeftButton:
            resize_direction = self._get_resize_direction(event.x(), event.y())
            if resize_direction:
                self.is_resizing = True
                self.resize_direction = resize_direction
                self.last_mouse_x = event.x()
                self.last_mouse_y = event.y()
            else:
                super().mousePressEvent(event)
            self.mouse_press_x = event.x()
            self.mouse_press_y = event.y()

    def mouseMoveEvent(self, event: QEvent) -> None:
        """Handle mouse move for cursor updates and resizing/dragging."""
        resize_direction = self._get_resize_direction(event.x(), event.y())
        cursor = self._get_cursor_for_direction(resize_direction)
        if cursor:
            self.setCursor(cursor)
        else:
            self.setCursor(Qt.ArrowCursor)

        if event.buttons() == Qt.LeftButton:
            if self.is_resizing:
                self._perform_resize(event)
            else:
                super().mouseMoveEvent(event)

    def _perform_resize(self, event: QEvent) -> None:
        """Handle window resizing based on drag direction."""
        new_x, new_y, new_width, new_height = self._calculate_new_geometry(
            event.globalPos().x(), event.globalPos().y()
        )

        self.setGeometry(new_x, new_y, new_width, new_height)
        self.last_mouse_x = event.x()
        self.last_mouse_y = event.y()

    def mouseReleaseEvent(self, event: QEvent) -> None:
        """Handle mouse release for resizing and dragging."""
        if event.button() == Qt.LeftButton:
            self.is_resizing = False
            self.resize_direction = ""
            super().mouseReleaseEvent(event)

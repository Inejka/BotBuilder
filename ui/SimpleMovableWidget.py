from PyQt6 import QtGui
from PyQt6.QtCore import Qt

from utils.KOSTYAWrapper import KostyaWrapper


def SimpleMovableWidget(cls):
    @KostyaWrapper
    class Wrapper(cls):
        def __init__(self, *args):
            self.touch_y = None
            self.touch_x = None
            self.is_moving = False
            self.have_end_move_callback = hasattr(self, "end_move_callback")

        def mousePressEvent(self, mouse_event: QtGui.QMouseEvent) -> None:
            if mouse_event.button() == Qt.MouseButton.MiddleButton:
                self.is_moving = True
                self.touch_x = mouse_event.scenePosition().x() - self.pos().x()
                self.touch_y = mouse_event.scenePosition().y() - self.pos().y()

            super().mousePressEvent(mouse_event)

        def mouseReleaseEvent(self, mouse_event: QtGui.QMouseEvent) -> None:
            if mouse_event.button() == Qt.MouseButton.MiddleButton:
                self.is_moving = False
                if self.have_end_move_callback:
                    self.end_move_callback()
            super().mouseReleaseEvent(mouse_event)

        def mouseMoveEvent(self, mouse_event: QtGui.QMouseEvent) -> None:
            if self.is_moving:
                self.move(int(mouse_event.scenePosition().x() - self.touch_x),
                          int(mouse_event.scenePosition().y() - self.touch_y))
                self.update_callback()
            super().mouseMoveEvent(mouse_event)

    return Wrapper

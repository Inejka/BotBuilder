from PyQt6.QtCore import Qt
from pyqt6_plugins.examplebuttonplugin import QtGui
from utils.KOSTYAWrapper import KostyaWrapper


def SimpleMovableWidget(cls):
    @KostyaWrapper
    class Wrapper(cls):
        def __init__(self, *args):
            self.is_moving = False
            self.have_end_move_callback = hasattr(self, "end_move_callback")

        def mousePressEvent(self, mouse_event: QtGui.QMouseEvent) -> None:
            if mouse_event.button() == Qt.MouseButtons.MiddleButton:
                self.is_moving = True
                self.touch_x = mouse_event.scenePosition().x() - self.pos().x()
                self.touch_y = mouse_event.scenePosition().y() - self.pos().y()

            super().mousePressEvent(mouse_event)

        def mouseReleaseEvent(self, mouse_event: QtGui.QMouseEvent) -> None:
            if mouse_event.button() == Qt.MouseButtons.MiddleButton:
                self.is_moving = False
                if self.have_end_move_callback:
                    self.end_move_callback()
            super().mouseReleaseEvent(mouse_event)

        def mouseMoveEvent(self, mouse_event: QtGui.QMouseEvent) -> None:
            if self.is_moving:
                self.move(mouse_event.scenePosition().x() + self.menu_offset_x() - self.touch_x,
                          mouse_event.scenePosition().y() + self.menu_offset_y() - self.touch_y)
                self.update_callback()
            super().mouseMoveEvent(mouse_event)

        def moveEvent(self, move_event: QtGui.QMoveEvent) -> None:
            self.moveEvent = super().moveEvent

    return Wrapper

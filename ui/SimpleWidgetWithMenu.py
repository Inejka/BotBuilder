from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QScrollArea, QFrame
from pyqt6_plugins.examplebuttonplugin import QtGui
from ui.SimpleMenuWithButtons import SimpleMenuWithButtons


class SimpleWidgetWithMenu(QFrame):
    def __init__(self, names_with_actions, menu_offset_x, menu_offset_y, parent=None):
        super().__init__(parent)
        self.menu = None
        self.names_with_actions = names_with_actions
        self.menu_offset_x = menu_offset_x
        self.menu_offset_y = menu_offset_y

    def set_names_with_actions(self, names_with_actions):
        self.names_with_actions = names_with_actions

    def mouseReleaseEvent(self, mouse_event: QtGui.QMouseEvent) -> None:
        if self.menu is not None:
            self.menu.setParent(None)
            self.menu = None
        if mouse_event.button() == Qt.MouseButtons.RightButton:
            self.menu = SimpleMenuWithButtons(self, self.names_with_actions)
            self.menu.show()
            mouse_position = mouse_event.scenePosition()
            self.menu.move(mouse_position.x() + self.menu_offset_x(),
                           mouse_position.y() + self.menu_offset_y())

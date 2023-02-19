from functools import partial

from PyQt6.QtWidgets import QFrame, QMenu
from PathFile import Paths
from utils.GetStyleFromFile import get_style


class SimpleWidgetWithMenu(QFrame):
    def __init__(self, names_with_actions, parent=None):
        super().__init__(parent)
        self.menu = None
        self.menu_pos = None
        self.names_with_actions = names_with_actions
        self.initMenu()
        self.setStyleSheet(get_style(Paths.SimpleWidgetWithMenu))

    def set_names_with_actions(self, names_with_actions):
        self.names_with_actions = names_with_actions
        self.initMenu()

    def initMenu(self):
        self.menu = QMenu(self)
        if self.names_with_actions is None or len(self.names_with_actions) == 0:
            return
        if len(self.names_with_actions[0]) == 3:
            for name, action, params in self.names_with_actions:
                action_menu = self.menu.addAction(name)
                action_menu.triggered.connect(partial(action, params))

        if len(self.names_with_actions[0]) == 2:
            for name, action in self.names_with_actions:
                action_menu = self.menu.addAction(name)
                action_menu.triggered.connect(action)

    def contextMenuEvent(self, event):
        self.menu_pos = event.pos()
        self.menu.exec(event.globalPos())

    def get_menu_pos(self):
        return self.menu_pos

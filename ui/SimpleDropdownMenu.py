from PyQt6 import QtGui
from PyQt6.QtWidgets import QVBoxLayout, QFrame, QPushButton
from functools import partial

from utils.GetStyleFromFile import get_style
from PathFile import Paths


class SimpleDropdownMenu(QFrame):
    def __init__(self, parent, names_with_actions):
        super().__init__(parent)
        self.layout = self.__get_layout()
        self.setLayout(self.layout)

        if len(names_with_actions[0]) == 3:
            for name, action, params in names_with_actions:
                button = QPushButton(name)
                if action is not None:
                    button.clicked.connect(partial(action, params))
                self.layout.addWidget(button)

        if len(names_with_actions[0]) == 2:
            for name, action in names_with_actions:
                button = QPushButton(name)
                if action is not None:
                    button.clicked.connect(action)
                self.layout.addWidget(button)

        self.setStyleSheet(get_style(Paths.SimpleMenuWithButtons.value))

    def __get_layout(self):
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(2, 2, 2, 2)
        return layout

    def mousePressEvent(self, mouse_even: QtGui.QMouseEvent) -> None:
        pass

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        pass

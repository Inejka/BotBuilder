from PyQt6.QtWidgets import QVBoxLayout, QFrame, QPushButton
from pyqt6_plugins.examplebuttonplugin import QtGui
from utils.GetStyleFromFile import get_style
from PathFile import Paths


class SimpleMenuWithButtons(QFrame):
    def __init__(self, parent, names_with_actions):
        super().__init__(parent)
        self.layout = self.__get_layout()
        self.setLayout(self.layout)

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
from collections.abc import Callable

from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QLabel, QLineEdit, QScrollArea, QVBoxLayout

from PathFile import Paths
from utils.GetStyleFromFile import get_style


class CommandLineOutput(QScrollArea):
    def __init__(self) -> None:
        super().__init__()
        self.inner_widget = QFrame()
        self.inner_widget_layout = QVBoxLayout()
        self.inner_widget.setLayout(self.inner_widget_layout)
        self.setWidget(self.inner_widget)
        self.inner_widget_layout.setSpacing(1)
        self.setWidgetResizable(True)
        self.inner_widget_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setStyleSheet(get_style(Paths.CommandLine))

    def add_text(self, text: str) -> None:
        label = QLabel(self.inner_widget)
        label.setText(text)
        self.inner_widget_layout.addWidget(label)


class CommandLineInput(QLineEdit):
    def __init__(self) -> None:
        super().__init__()
        self.commands = {}
        self.setStyleSheet(get_style(Paths.CommandLineInput))

    def keyReleaseEvent(self, key_event: QtGui.QKeyEvent) -> None:
        if key_event.key() == Qt.Key.Key_Return.value:
            if self.text() in self.commands:
                self.commands[self.text()]()
            self.clear()

    def set_commands(self, commands: dict) -> None:
        self.commands = commands

    def add_command(self, key: str, value: Callable) -> None:
        self.commands[key] = value


class CommandLine(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.input = CommandLineInput()
        self.output = CommandLineOutput()
        self.layout.addWidget(self.output)
        self.layout.addWidget(self.input)

    def get_input(self) -> CommandLineInput:
        return self.input

    def get_output(self) -> CommandLineOutput:
        return self.output

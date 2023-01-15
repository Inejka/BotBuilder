from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QSplitter
from ui.BotBuilderWindow import BotBuilderWindow
from ui.CommandLine import CommandLine


class CentralWidget(QSplitter):
    def __init__(self):
        super().__init__()
        self.bot_builder_window = BotBuilderWindow()
        self.command_line = CommandLine()
        self.setOrientation(Qt.Orientations.Vertical)
        self.addWidget(self.bot_builder_window)
        self.addWidget(self.command_line)

    def get_bot_builder_window(self) -> BotBuilderWindow:
        return self.bot_builder_window

    def get_command_line(self) -> CommandLine:
        return self.command_line

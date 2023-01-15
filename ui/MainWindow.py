from PyQt6.QtWidgets import QMainWindow
from ui.BotBuilderWindow import BotBuilderWindow
from ui.CentralWidget import CentralWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Bot builder app")
        self.setStyleSheet("""
        QMainWindow{
    border: 1px blue;
    width: fit-content;
    block-size: fit-content;
    background-color: grey;
    color:grey;
    }
        """)

        self.central_widget = CentralWidget()
        self.setCentralWidget(self.central_widget)

    def get_bot_builder_window(self) -> BotBuilderWindow:
        return self.central_widget.get_bot_builder_window()

    def get_central_widget(self) -> CentralWidget:
        return self.central_widget

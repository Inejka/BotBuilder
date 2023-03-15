from bot.Bot import Bot
from controllers.CommandLineController import CommandLineController
from controllers.UIController import UIController
from ui.MainWindow import MainWindow
from ui.UiInitializer import initialize_ui


class MainController:
    def __init__(self) -> None:
        self.UIController = None
        self.CommandLineController = None
        self.app = None
        self.bot = None
        self.MainWindow = None

    def start(self) -> None:
        self.app, self.MainWindow = initialize_ui()
        self.bot = Bot()
        self.CommandLineController = CommandLineController(self)
        self.UIController = UIController(self.bot, self.MainWindow)
        self.app.exec()

    def get_main_window(self) -> MainWindow:
        return self.MainWindow

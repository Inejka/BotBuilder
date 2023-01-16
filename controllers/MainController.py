from bot.Bot import Bot
from controllers.UIController import UIController
from ui.UiInitializer import initialize_ui
from controllers.CommandLineController import CommandLineController


class MainController:
    def __init__(self):
        self.UIController = None
        self.CommandLineController = None
        self.app = None
        self.bot = None
        self.MainWindow = None

    def start(self):
        self.app, self.MainWindow = initialize_ui()
        self.bot = Bot()
        self.CommandLineController = CommandLineController(self)
        self.UIController = UIController(self.bot, self.MainWindow)
        self.app.exec()

    def get_main_window(self):
        return self.MainWindow

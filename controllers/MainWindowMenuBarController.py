import os

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QFileDialog

from PathFile import Paths
from bot.Bot import Bot
from ui.MainWindow import MainWindow
from utils.GetStyleFromFile import get_style


class MainWindowMenuBarController:
    def __init__(self, bot: Bot, mainWindow: MainWindow, ui_controller: "UIController") -> None:
        self.bot = bot
        self.mainWindow = mainWindow
        self.uiController = ui_controller
        self.init_menu_bar()

    def init_menu_bar(self) -> None:
        menu_bar = self.mainWindow.menuBar()
        menu_bar.setStyleSheet(get_style(Paths.MainWindowMenuBar))
        file_menu = menu_bar.addMenu("&File")

        select_folder_action = QAction("Select working folder", self.mainWindow)
        select_folder_action.triggered.connect(self.select_folder)

        clear_action = QAction("Clear", self.mainWindow)
        clear_action.triggered.connect(self.clear)
        clear_action.setShortcut("Ctrl+r")

        save_action = QAction("Save", self.mainWindow)
        save_action.triggered.connect(self.save)
        save_action.setShortcut("Ctrl+s")

        load_action = QAction("Load", self.mainWindow)
        load_action.triggered.connect(self.load)
        load_action.setShortcut("Ctrl+o")

        file_menu.addAction(select_folder_action)
        file_menu.addAction(save_action)
        file_menu.addAction(load_action)
        file_menu.addAction(clear_action)

    def clear(self) -> None:
        self.bot.clear()
        self.uiController.clear()

    def select_folder(self) -> None:
        file = QFileDialog.getExistingDirectory(self.mainWindow, "Select Directory",
                                                os.path.abspath(Paths.BotGeneratedFolder))
        if file:
            # self.clear()
            Paths.BotGeneratedFolder = file

    def save(self) -> None:
        self.bot.save()
        self.uiController.save()

    def load(self) -> None:
        self.clear()
        self.bot.load()
        self.uiController.load()

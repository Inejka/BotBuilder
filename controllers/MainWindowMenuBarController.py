from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QFileDialog

from bot.Bot import Bot
from ui.MainWindow import MainWindow
from PathFile import Paths
from utils.GetStyleFromFile import get_style
import os


class MainWindowMenuBarController:
    def __init__(self, bot: Bot, mainWindow: MainWindow, uiController):
        self.bot = bot
        self.mainWindow = mainWindow
        self.uiController = uiController
        self.init_menu_bar()

    def init_menu_bar(self):
        menuBar = self.mainWindow.menuBar()
        menuBar.setStyleSheet(get_style(Paths.MainWindowMenuBar))
        fileMenu = menuBar.addMenu('&File')

        selectFolderAction = QAction("Select working folder", self.mainWindow)
        selectFolderAction.triggered.connect(self.select_folder)

        clearAction = QAction("Clear", self.mainWindow)
        clearAction.triggered.connect(self.clear)

        fileMenu.addAction(selectFolderAction)
        fileMenu.addAction(clearAction)

    def clear(self):
        self.bot.clear()
        self.uiController.clear()

    def select_folder(self):
        file = QFileDialog.getExistingDirectory(self.mainWindow, "Select Directory",
                                                os.path.abspath(Paths.BotGeneratedFolder))
        if file:
            self.clear()
            Paths.BotGeneratedFolder = file

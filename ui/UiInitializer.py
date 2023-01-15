from PyQt6.QtWidgets import QApplication, QWidget
from ui.MainWindow import MainWindow
import sys


def initialize_ui() -> MainWindow:
    app = QApplication(sys.argv)
    temp = MainWindow()
    temp.show()
    return app, temp


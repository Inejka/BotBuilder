import sys

from PyQt6.QtWidgets import QApplication

from ui.MainWindow import MainWindow


def initialize_ui() -> (QApplication, MainWindow):
    app = QApplication(sys.argv)
    temp = MainWindow()
    temp.show()
    return app, temp

import math

from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPen, QBrush
from PyQt6.QtWidgets import QScrollArea

from PathFile import Paths
from ui.SimpleWidgetWithMenu import SimpleWidgetWithMenu
from utils.GetStyleFromFile import get_style
from utils.LinesWrapper import LinesWrapper


class BotBuilderWindow(QScrollArea):
    def __init__(self):
        super().__init__()
        self.inner_widget = None
        self.init_ui()
        self.lines = LinesWrapper(self.inner_widget.update)
        self.transit_thickness = 5
        self.lines_equations = {}

    def init_ui(self):
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.inner_widget = SimpleWidgetWithMenu([])

        def set_menu(menu):
            self.inner_widget.menu = menu

        self.inner_widget.set_menu = set_menu
        self.inner_widget.get_menu = lambda: self.inner_widget.menu

        self.setWidget(self.inner_widget)
        self.inner_widget.setGeometry(0, 0, 10000, 10000)
        self.inner_widget.paintEvent = self.paintEvent
        self.inner_widget.mouseMoveEvent = self.mouseMoveEvent
        self.setStyleSheet(get_style(Paths.BotBuilderWindow))

    def get_lines_wrapper(self) -> LinesWrapper:
        return self.lines

    def set_menu_names_with_actions(self, names_with_actions):
        self.inner_widget.set_names_with_actions(names_with_actions)

    def get_inner_widget(self) -> SimpleWidgetWithMenu:
        return self.inner_widget

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self.inner_widget)
        self.draw_lines(qp)
        qp.end()

    def draw_lines(self, qp):
        pen = QPen(Qt.GlobalColor.black, self.transit_thickness, Qt.PenStyle.SolidLine)

        qp.setPen(pen)
        for from_point, to_point in self.lines:
            qp.drawLine(int(from_point[0]), int(from_point[1]), int(to_point[0]), int(to_point[1]))
            qp.setBrush(QBrush(Qt.GlobalColor.yellow, Qt.BrushStyle.SolidPattern))
            qp.drawRect(int(to_point[0] - 10), int(to_point[1] - 10), 20, 20)

    def mouseDoubleClickEvent(self, mouse_event: QtGui.QMouseEvent) -> None:
        for k, b in self.lines_equations.values():
            if math.fabs((
                                 mouse_event.scenePosition().y() - b) / k - mouse_event.scenePosition().x()) < self.transit_thickness:
                print("DD")

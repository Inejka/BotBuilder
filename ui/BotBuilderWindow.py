import math

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPen, QBrush
from PyQt6.QtWidgets import QScrollArea
from pyqt6_plugins.examplebuttonplugin import QtGui

from ui.SimpleWidgetWithMenu import SimpleWidgetWithMenu
from utils.LinesWrapper import LinesWrapper
from PathFile import Paths
from utils.GetStyleFromFile import get_style


class BotBuilderWindow(QScrollArea):
    def __init__(self):
        super().__init__()
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.inner_widget = SimpleWidgetWithMenu([], self.get_x_offset,
                                                 self.get_y_offset)
        self.setWidget(self.inner_widget)
        self.inner_widget.setGeometry(0, 0, 10000, 10000)
        self.inner_widget.paintEvent = self.paintEvent
        self.inner_widget.mouseMoveEvent = self.mouseMoveEvent
        self.lines = LinesWrapper(self.inner_widget.update)
        self.transit_thickness = 5
        self.lines_equations = {}
        self.setStyleSheet(get_style(Paths.BotBuilderWindow.value))

    def get_lines_wrapper(self) -> LinesWrapper:
        return self.lines

    def get_x_offset(self):
        return self.horizontalScrollBar().value()

    def get_y_offset(self):
        return self.verticalScrollBar().value()

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
            qp.drawLine(from_point[0], from_point[1], to_point[0], to_point[1])
            qp.setBrush(QBrush(Qt.GlobalColor.yellow, Qt.BrushStyle.SolidPattern))
            qp.drawRect(to_point[0] - 10, to_point[1] - 10, 20, 20)

    def mouseDoubleClickEvent(self, mouse_event: QtGui.QMouseEvent) -> None:
        for k, b in self.lines_equations.values():
            if math.fabs((
                                 mouse_event.scenePosition().y() - b) / k - mouse_event.scenePosition().x()) < self.transit_thickness:
                print("DD")

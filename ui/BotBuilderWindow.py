import math

from PyQt6 import QtGui
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPainter, QPen, QBrush
from PyQt6.QtWidgets import QScrollArea, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsItem

from PathFile import Paths
from ui.SimpleWidgetWithMenu import SimpleWidgetWithMenu
from utils.GetStyleFromFile import get_style
from utils.LinesWrapper import LinesWrapper


@SimpleWidgetWithMenu
class BotBuilderWindow(QGraphicsView):
    # todo implement movement by left click or middle button
    # todo implement auto resize
    # todo implement area selection and movement
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.lines = LinesWrapper(self.update)
        self.transit_thickness = 5
        self.lines_equations = {}
        self.scene_s = QGraphicsScene()
        self.setScene(self.scene_s)

        rect = QGraphicsRectItem(0, 0, 200, 50)
        rect.setPos(50, 20)
        brush = QBrush(Qt.GlobalColor.red)
        rect.setBrush(brush)

        # Define the pen (line)
        pen = QPen(Qt.GlobalColor.cyan)
        pen.setWidth(10)
        rect.setPen(pen)
        self.scene_s.addItem(rect)
        for item in self.scene_s.items():
            item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
            item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)

    def init_ui(self):
        self.setStyleSheet(get_style(Paths.BotBuilderWindow))

    def add_item(self, item):
        self.scene().addItem(item)

    def add_widget(self, widget):
        return self.scene().addWidget(widget)

    def get_lines_wrapper(self) -> LinesWrapper:
        return self.lines

    def custom_map(self, point):
        return self.mapToScene(point)

    # def paintEvent(self, e):
    #     qp = QPainter()
    #     qp.begin(self)
    #     self.draw_lines(qp)
    #     #todo create transit_ui widget and move paint logit to it
    #     qp.end()
    #
    # def draw_lines(self, qp):
    #     pen = QPen(Qt.GlobalColor.black, self.transit_thickness, Qt.PenStyle.SolidLine)
    #
    #     qp.setPen(pen)
    #     for from_point, to_point in self.lines:
    #         qp.drawLine(int(from_point[0]), int(from_point[1]), int(to_point[0]), int(to_point[1]))
    #         qp.setBrush(QBrush(Qt.GlobalColor.yellow, Qt.BrushStyle.SolidPattern))
    #         qp.drawRect(int(to_point[0] - 10), int(to_point[1] - 10), 20, 20)

    # def mouseDoubleClickEvent(self, mouse_event: QtGui.QMouseEvent) -> None:
    #     for k, b in self.lines_equations.values():
    #         if math.fabs((
    #                              mouse_event.scenePosition().y() - b) / k - mouse_event.scenePosition().x()) < self.transit_thickness:
    #             print("DD")

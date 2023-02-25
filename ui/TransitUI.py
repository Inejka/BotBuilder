import math
import typing
from random import random, randint

from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPen, QBrush, QPainterPath, QColor
from PyQt6.QtWidgets import QGraphicsEllipseItem, QGraphicsItem, QGraphicsSceneMouseEvent, QGraphicsPathItem, QWidget


class Circle(QGraphicsEllipseItem):
    def __init__(self, x, y, w, h, color: Qt.GlobalColor, move_callback):
        super().__init__(x, y, w, h)
        self.offset = None
        self.center_point = QPointF(w / 2, h / 2)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsScenePositionChanges, True)
        self.setPen(QPen(Qt.GlobalColor.cyan))
        self.setBrush(QBrush(color))
        self.move_callback = move_callback
        self.z_level = 2
        self.setZValue(self.z_level)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.ungrabMouse()
        for item in self.scene().items(self.get_center()):
            if item.__class__.__name__ == "StateUIProxy":
                self.bind_to_stateUI(item.get_state_ui())
                break
        super().mouseReleaseEvent(event)

    def get_center(self):
        return self.scenePos() + self.center_point

    def itemChange(self, change: 'QGraphicsItem.GraphicsItemChange', value: typing.Any) -> typing.Any:
        if change == QGraphicsItem.GraphicsItemChange.ItemScenePositionHasChanged:
            self.move_callback(self.get_center())
        return super().itemChange(change, value)

    def bind_to_stateUI(self, state) -> None:
        scenePos = self.scenePos()
        self.setParentItem(state.get_proxy())
        self.setPos(scenePos - state.get_proxy().scenePos())


class Line(QGraphicsPathItem):
    def __init__(self, from_point: QPointF = None, to_point: QPointF = None):
        super().__init__()
        self.width = 3
        self.pen = QPen(Qt.GlobalColor.cyan)
        self.pen.setWidth(self.width)
        self.setAcceptHoverEvents(True)
        self.from_point = from_point
        self.to_point = to_point
        self.z_level = 1
        self.setZValue(self.z_level)

    def get_path(self) -> QPainterPath:
        self.get_path = self.straight_path
        return self.straight_path()

    def straight_path(self) -> QPainterPath:
        to_return = QPainterPath(self.from_point)
        to_return.lineTo(self.to_point)
        return to_return

    def set_from_point(self, point: QPointF):
        self.from_point = point

    def set_to_point(self, point: QPointF):
        self.to_point = point

    def hoverMoveEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        super().hoverMoveEvent(event)

    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionGraphicsItem',
              widget: typing.Optional[QWidget] = ...) -> None:
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        painter.setPen(self.pen)
        path = self.get_path()
        self.setPath(path)
        painter.drawPath(path)

    def shape(self) -> QtGui.QPainterPath:
        qp = QtGui.QPainterPathStroker()
        qp.setWidth(self.width)
        qp.setCapStyle(QtCore.Qt.PenCapStyle.SquareCap)
        shape = qp.createStroke(self.path())
        return shape


class TransitUI:
    def __init__(self, point, scene, state):
        self.path = Line(point, point)
        scene.addItem(self.path)
        self.end_circle = Circle(0, 0, 10, 10, Qt.GlobalColor.red, self.path.set_to_point)
        self.end_circle.setPos(point.x() - 5, point.y() - 5)
        scene.addItem(self.end_circle)
        self.start_circle = Circle(0, 0, 10, 10,
                                   Qt.GlobalColor.darkGreen,
                                   self.path.set_from_point)
        scene.addItem(self.start_circle)
        self.start_circle.setPos(point - self.start_circle.center_point)
        self.start_circle.bind_to_stateUI(state)

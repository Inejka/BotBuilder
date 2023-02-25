import math
import typing
from random import random, randint

from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPen, QBrush, QPainterPath, QColor
from PyQt6.QtWidgets import QGraphicsEllipseItem, QGraphicsItem, QGraphicsSceneMouseEvent, QGraphicsPathItem, QWidget


class Circle(QGraphicsEllipseItem):
    def __init__(self, x, y, w, h, color: Qt.GlobalColor, move_callback, transit):
        super().__init__(x, y, w, h)
        self.start_mouse_click_position = None
        self.offset = None
        self.center_point = QPointF(w / 2, h / 2)

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsScenePositionChanges, True)
        self.setPen(QPen(Qt.GlobalColor.cyan))
        self.setBrush(QBrush(color))

        self.state_id = None
        self.move_callback = move_callback
        self.transit = transit

        self.z_level = 2
        self.setZValue(self.z_level)

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        self.start_mouse_click_position = self.pos()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        founded_state_to_bind = False
        for item in self.scene().items(self.get_center()):
            if item.__class__.__name__ == "StateUIProxy":
                self.bind_to_stateUI(item.get_state_ui())
                founded_state_to_bind = True
                # after creation of transit i force input to end_circle, so it's mouseReleaseEvent will be fired first
                # thats, if i found StateUiProxy, i bind end_circle to it and assume that transit created
                self.transit.update_transit()
        if not founded_state_to_bind:
            self.setPos(self.start_mouse_click_position)
        super().mouseReleaseEvent(event)
        self.ungrabMouse()
        if not founded_state_to_bind and not self.transit.is_created:
            self.transit.destroy()

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
        self.state_id = state.get_state_id()

    def get_state_id(self):
        return self.state_id


class Line(QGraphicsPathItem):
    def __init__(self, from_point: QPointF = None, to_point: QPointF = None):
        super().__init__()

        self.from_point = from_point
        self.to_point = to_point
        self.width = 3

        self.pen = QPen(Qt.GlobalColor.cyan)
        self.pen.setWidth(self.width)
        self.setAcceptHoverEvents(True)

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
    def __init__(self, point, scene, state, create_transit_callback):
        self.path = Line(point, point)
        self.end_circle = Circle(0, 0, 10, 10, Qt.GlobalColor.red, self.path.set_to_point, self)
        self.start_circle = Circle(0, 0, 10, 10, Qt.GlobalColor.darkGreen, self.path.set_from_point, self)

        self.end_circle.setPos(point.x() - 5, point.y() - 5)
        self.start_circle.setPos(point - self.start_circle.center_point)
        self.start_circle.bind_to_stateUI(state)
        self.is_created = False

        scene.addItem(self.path)
        scene.addItem(self.end_circle)
        scene.addItem(self.start_circle)

        self.create_transit_callback = create_transit_callback
        self.name = None
        self.transit_id = None

    def destroy(self):
        self.path.scene().removeItem(self.path)
        # if because transitUi is cleared first, and it removes it child
        if self.end_circle.scene():
            self.end_circle.scene().removeItem(self.end_circle)
        if self.start_circle.scene():
            self.start_circle.scene().removeItem(self.start_circle)

    def update_transit(self):
        if not self.is_created:
            self.is_created = True
            self.create_transit_callback(self)

    def get_from_state_id(self):
        return self.start_circle.get_state_id()

    def get_to_state_id(self):
        return self.end_circle.get_state_id()

    def set_id(self, id):
        self.transit_id = id

    def set_name(self, name):
        self.name = name

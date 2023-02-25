import json
import typing

from PyQt6 import QtGui
from PyQt6.QtCore import Qt, QPointF, QObject, QEvent, QPoint
from PyQt6.QtGui import QPen, QBrush
from PyQt6.QtWidgets import QLineEdit, QVBoxLayout, QFrame, QGraphicsRectItem, QGraphicsItem, QWidget, \
    QGraphicsSceneContextMenuEvent, QGraphicsSceneMouseEvent, QGraphicsProxyWidget

from PathFile import Paths
from ui.SimpleWidgetWithMenu import SimpleWidgetWithMenu
from ui.TransitUI import TransitUI
from utils.GetStyleFromFile import get_style
from utils.LinesWrapper import Line, Point


class StateUIProxy(QGraphicsProxyWidget):
    def __init__(self, state_ui):
        super().__init__()
        self.state_ui = state_ui
        self.setWidget(state_ui)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        super().mousePressEvent(event)
        if not event.isAccepted():
            self.state_ui.recent_transit_ui.end_circle.grabMouse()
            self.state_ui.recent_transit_ui.end_circle.mousePressEvent(event)
            event.accept()

    def get_state_ui(self):
        return self.state_ui


class ControlRectangle(QGraphicsRectItem):
    def __init__(self, w, stateUi, h=10):
        super().__init__(0, 0, w, h)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        # self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setPen(QPen(Qt.GlobalColor.cyan))
        self.setBrush(QBrush(Qt.GlobalColor.darkGreen))
        self.stateUI = stateUi

    def contextMenuEvent(self, event: QGraphicsSceneContextMenuEvent) -> None:
        self.stateUI.menu_pos = event.pos() if self.stateUI.custom_map is None else self.stateUI.custom_map(event.pos())
        self.stateUI.menu.exec(QPoint(int(event.screenPos().x()), int(event.screenPos().y())))
        event.accept()


@SimpleWidgetWithMenu
class StateUI(QFrame):
    def __init__(self, state_name, lines, state_id,
                 try_create_transit_callback, update_line_callback, try_open_editor_callback):
        super().__init__()
        self.scene_control_proxy = None
        self.scene_proxy = None
        self.state_name_input = None
        self.layout = None
        self.creating_line = None
        self.state_id = state_id
        self.update_line_callback = update_line_callback
        self.state_name = state_name
        self.lines = lines
        self.try_open_editor_callback = try_open_editor_callback
        self.try_create_transit_callback = try_create_transit_callback
        self.update_callback = self.lines.update_callback
        self.point_with_offset = {}
        self.recent_transit_ui = None
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.state_name_input = QLineEdit()
        self.state_name_input.mouseDoubleClickEvent = self.mouseDoubleClickEvent
        self.layout.addWidget(self.state_name_input)
        self.state_name_input.editingFinished.connect(self.edit_state_name_reaction)
        self.setLayout(self.layout)
        self.state_name_input.setText(self.state_name.get())
        self.setStyleSheet(get_style(Paths.StateUI))

    def get_state_id(self):
        return self.state_id

    def edit_state_name_reaction(self):
        self.state_name.set_str(self.state_name_input.text())

    def mousePressEvent(self, mouse_event: QtGui.QMouseEvent) -> None:
        mouse_event.ignore()
        self.recent_transit_ui = TransitUI(self.scene_proxy.mapToScene(QPointF(mouse_event.pos())),
                                           self.scene_proxy.scene(), self)
        if mouse_event.button() == Qt.MouseButton.LeftButton:
            self.creating_line = Line(self.update_callback, self.state_id,
                                      self.mapToParent(mouse_event.pos()).x(),
                                      self.mapToParent(mouse_event.pos()).y(),
                                      self.mapToParent(mouse_event.pos()).x(),
                                      self.mapToParent(mouse_event.pos()).y())
            self.lines.add_line(self.creating_line)

    def mouseReleaseEvent(self, mouse_event: QtGui.QMouseEvent) -> None:
        # todo fix right click and creating line bug
        # todo fix move state over screen
        super().mouseReleaseEvent(mouse_event)
        if mouse_event.button() == Qt.MouseButton.LeftButton:
            self.try_create_transit_callback(self.creating_line)
            self.creating_line = None

    def mouseMoveEvent(self, mouse_event: QtGui.QMouseEvent) -> None:
        if not self.creating_line is None:
            self.creating_line[1][0] = self.mapToParent(mouse_event.pos()).x()
            self.creating_line[1][1] = self.mapToParent(mouse_event.pos()).y()

    def moveEvent(self, move_event: QtGui.QMoveEvent) -> None:
        for i, j in self.point_with_offset.items():
            i[0] = move_event.pos().x() - j[0]
            i[1] = move_event.pos().y() - j[1]

    def add_point_with_offset(self, point, offset):
        self.point_with_offset[point] = offset

    def mouseDoubleClickEvent(self, mouse_event: QtGui.QMouseEvent) -> None:
        if mouse_event.button() == Qt.MouseButton.LeftButton:
            self.try_open_editor_callback(self.state_id)

    def end_move_callback(self):
        for i, _ in self.point_with_offset.items():
            self.update_line_callback(i.get_transit_parent_id())

    def to_json(self):
        # json loads for bot serialization for not to return a str
        # todo find way to remove json loads
        to_return = "{"
        to_return += '"state_id":"' + self.state_id + '"'
        to_return += ',"pos_x":' + str(self.scene_control_proxy.pos().x())
        to_return += ',"pos_y":' + str(self.scene_control_proxy.pos().y())
        temp = [{"point": f, "offset": t} for f, t in self.point_with_offset.items()]
        to_return += ',"point_with_offset":' + json.dumps(temp, default=Point.to_json)
        to_return += "}"
        return json.loads(to_return)

    def bind_proxies(self, control_proxy, proxy):
        self.scene_control_proxy = control_proxy
        self.scene_proxy = proxy
        # control_proxy.contextMenuEvent = self.contextMenuEvent
        # proxy.contextMenuEvent = self.contextMenuEvent

    def get_control_proxy(self):
        return self.scene_control_proxy

    def get_proxy(self):
        return self.scene_proxy

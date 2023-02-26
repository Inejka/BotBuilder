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
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setPen(QPen(Qt.GlobalColor.cyan))
        self.setBrush(QBrush(Qt.GlobalColor.darkGreen))
        self.stateUI = stateUi

    def contextMenuEvent(self, event: QGraphicsSceneContextMenuEvent) -> None:
        self.stateUI.menu_pos = event.pos() if self.stateUI.custom_map is None else self.stateUI.custom_map(event.pos())
        self.stateUI.menu.exec(QPoint(int(event.screenPos().x()), int(event.screenPos().y())))
        event.accept()


@SimpleWidgetWithMenu
class StateUI(QFrame):
    def __init__(self, state_name, state_id, create_transit_callback, try_open_editor_callback):
        super().__init__()
        self.scene_control_proxy = None
        self.scene_proxy = None
        self.state_name_input = None
        self.layout = None
        self.state_id = state_id
        self.state_name = state_name
        self.try_open_editor_callback = try_open_editor_callback
        self.create_transit_callback = create_transit_callback
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
        if mouse_event.button() == Qt.MouseButton.LeftButton:
            self.recent_transit_ui = TransitUI(self.scene_proxy.mapToScene(QPointF(mouse_event.pos())),
                                               self.scene_proxy.scene(), self, self.create_transit_callback)
            mouse_event.ignore()

    def mouseDoubleClickEvent(self, mouse_event: QtGui.QMouseEvent) -> None:
        if mouse_event.button() == Qt.MouseButton.LeftButton:
            self.try_open_editor_callback(self.state_id)

    def to_json(self):
        # json loads for bot serialization for not to return a str
        # todo find way to remove json loads
        to_return = "{"
        to_return += '"state_id":"' + self.state_id + '"'
        to_return += ',"pos_x":' + str(self.scene_control_proxy.pos().x())
        to_return += ',"pos_y":' + str(self.scene_control_proxy.pos().y())
        to_return += "}"
        return json.loads(to_return)

    def bind_proxies(self, control_proxy, proxy):
        self.scene_control_proxy = control_proxy
        self.scene_proxy = proxy

    def get_control_proxy(self):
        return self.scene_control_proxy

    def get_proxy(self):
        return self.scene_proxy

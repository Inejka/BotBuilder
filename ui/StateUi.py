import json
import typing
from dataclasses import dataclass

from PyQt6 import QtGui
from PyQt6.QtCore import QPoint, QPointF, Qt
from PyQt6.QtGui import QBrush, QPen
from PyQt6.QtWidgets import (
    QFrame,
    QGraphicsItem,
    QGraphicsProxyWidget,
    QGraphicsRectItem,
    QGraphicsSceneContextMenuEvent,
    QGraphicsSceneMouseEvent,
    QLineEdit,
    QVBoxLayout,
)

from PathFile import Paths
from ui.SimpleWidgetWithMenu import SimpleWidgetWithMenu
from ui.TransitUI import TransitUI
from utils.GetStyleFromFile import get_style
from utils.StrWrapper import StrWrapper


class StateUIProxy(QGraphicsProxyWidget):
    def __init__(self, state_ui: "StateUI") -> None:
        super().__init__()
        self.state_ui = state_ui
        self.setWidget(state_ui)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        super().mousePressEvent(event)
        if not event.isAccepted():
            self.state_ui.recent_transit_ui.end_circle.grabMouse()
            self.state_ui.recent_transit_ui.end_circle.mousePressEvent(event)
            event.accept()

    def get_state_ui(self) -> "StateUI":
        return self.state_ui

    def contextMenuEvent(self, event: QGraphicsSceneContextMenuEvent) -> None:
        self.state_ui.menu_pos = event.pos() if self.state_ui.custom_map is None else self.state_ui.custom_map(
            event.pos())
        self.state_ui.menu.exec(QPoint(int(event.screenPos().x()), int(event.screenPos().y())))
        event.accept()


class ControlRectangle(QGraphicsRectItem):
    def __init__(self, w: int, state_ui: "StateUI", h: int = 10) -> None:
        super().__init__(0, 0, w, h)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setPen(QPen(Qt.GlobalColor.cyan))
        self.setBrush(QBrush(Qt.GlobalColor.darkGreen))
        self.state_ui = state_ui

    def contextMenuEvent(self, event: QGraphicsSceneContextMenuEvent) -> None:
        self.state_ui.menu_pos = event.pos() if self.state_ui.custom_map is None else self.state_ui.custom_map(
            event.pos())
        self.state_ui.menu.exec(QPoint(int(event.screenPos().x()), int(event.screenPos().y())))
        event.accept()

    def mouseDoubleClickEvent(self, event: "QGraphicsSceneMouseEvent") -> None:
        self.state_ui.try_open_editor_callback(self.state_ui.get_state_id())


@SimpleWidgetWithMenu
class StateUI(QFrame):
    @dataclass
    class StateUIParams:
        state_name: StrWrapper
        state_id: str
        try_open_editor_callback: typing.Callable
        generate_transit_callback: typing.Callable

    def __init__(self, params: StateUIParams) -> None:
        super().__init__()
        self.scene_control_proxy = None
        self.scene_proxy = None
        self.state_name_input = None
        self.layout = None
        self.state_id = params.state_id
        self.state_name = params.state_name
        self.try_open_editor_callback = params.try_open_editor_callback
        self.generate_transit_callback = params.generate_transit_callback
        self.recent_transit_ui = None
        self.init_ui()

    def init_ui(self) -> None:
        self.layout = QVBoxLayout()
        self.state_name_input = QLineEdit()
        self.state_name_input.mouseDoubleClickEvent = self.mouseDoubleClickEvent
        self.layout.addWidget(self.state_name_input)
        self.state_name_input.editingFinished.connect(self.edit_state_name_reaction)
        self.setLayout(self.layout)
        self.state_name_input.setText(self.state_name.get())
        self.setStyleSheet(get_style(Paths.StateUI))

    def get_state_id(self) -> str:
        return self.state_id

    def edit_state_name_reaction(self) -> None:
        self.state_name.set_str(self.state_name_input.text())

    def mousePressEvent(self, mouse_event: QtGui.QMouseEvent) -> None:
        if mouse_event.button() == Qt.MouseButton.LeftButton:
            self.recent_transit_ui = self.generate_transit_callback(
                TransitUI.TransitUIParams(self.scene_proxy.mapToScene(QPointF(mouse_event.pos())),
                                          self.scene_proxy.scene(), self))
            mouse_event.ignore()

    def mouseDoubleClickEvent(self, mouse_event: QtGui.QMouseEvent) -> None:
        if mouse_event.button() == Qt.MouseButton.LeftButton:
            self.try_open_editor_callback(self.state_id)

    def to_json(self) -> dict:
        # json loads for bot serialization for not to return a str
        # todo find way to remove json loads
        to_return = "{"
        to_return += '"state_id":"' + self.state_id + '"'
        to_return += ',"pos_x":' + str(self.scene_control_proxy.pos().x())
        to_return += ',"pos_y":' + str(self.scene_control_proxy.pos().y())
        to_return += "}"
        return json.loads(to_return)

    def bind_proxies(self, control_proxy: ControlRectangle, proxy: StateUIProxy) -> None:
        self.scene_control_proxy = control_proxy
        self.scene_proxy = proxy
        control_proxy

    def get_control_proxy(self) -> ControlRectangle:
        return self.scene_control_proxy

    def get_proxy(self) -> StateUIProxy:
        return self.scene_proxy

    def destroy(self) -> None:
        self.scene_control_proxy.scene().removeItem(self.scene_control_proxy)

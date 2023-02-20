import json

from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLineEdit, QVBoxLayout

from PathFile import Paths
from ui.SimpleMovableWidget import SimpleMovableWidget
from ui.SimpleWidgetWithMenu import SimpleWidgetWithMenu
from utils.GetStyleFromFile import get_style
from utils.LinesWrapper import Line, Point


@SimpleMovableWidget
class StateUI(SimpleWidgetWithMenu):
    def __init__(self, parent, state_name, lines, state_id,
                 try_create_transit_callback, update_line_callback, try_open_editor_callback):
        super().__init__(None, parent)
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
        self.show()

    def get_state_id(self):
        return self.state_id

    def edit_state_name_reaction(self):
        self.state_name.set_str(self.state_name_input.text())

    def mousePressEvent(self, mouse_event: QtGui.QMouseEvent) -> None:
        if mouse_event.button() == Qt.MouseButton.LeftButton:
            self.creating_line = Line(self.update_callback, self.state_id,
                                      self.mapToParent(mouse_event.pos()).x(),
                                      self.mapToParent(mouse_event.pos()).y(),
                                      self.mapToParent(mouse_event.pos()).x(),
                                      self.mapToParent(mouse_event.pos()).y())
            self.lines.add_line(self.creating_line)

    def mouseReleaseEvent(self, mouse_event: QtGui.QMouseEvent) -> None:
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
        to_return += ',"pos_x":' + str(self.pos().x())
        to_return += ',"pos_y":' + str(self.pos().y())
        temp = [{"point": f, "offset": t} for f, t in self.point_with_offset.items()]
        to_return += ',"point_with_offset":' + json.dumps(temp, default=Point.to_json)
        to_return += "}"
        return json.loads(to_return)

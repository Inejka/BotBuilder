import typing
from dataclasses import dataclass

from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import Qt, QPointF, QPoint
from PyQt6.QtGui import QPen, QBrush, QPainterPath, QFont, QIntValidator
from PyQt6.QtWidgets import QGraphicsEllipseItem, QGraphicsItem, QGraphicsSceneMouseEvent, QGraphicsPathItem, QWidget, \
    QGraphicsScene, QHBoxLayout, QGraphicsProxyWidget, QLineEdit

from ui.SimpleWidgetWithMenu import SimpleWidgetWithMenu
from utils.StrWrapper import StrWrapper


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
        self.scene().clearSelection()
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
    def __init__(self, from_point: QPointF = None, to_point: QPointF = None, transit=None):
        super().__init__()
        self.from_point = from_point
        self.to_point = to_point
        self.width = 3

        self.pen = QPen(Qt.GlobalColor.cyan)
        self.pen.setWidth(self.width)

        self.z_level = 1
        self.setZValue(self.z_level)
        self.transit = transit

        self.name_edit_params = [100, 13]
        self.priority_edit_params = [20, 13]
        self.q_line_edit_center = QPointF(self.name_edit_params[0] / 2, self.name_edit_params[1] / 2)
        self.q_line_edit_z = 3
        self.qwidget = QWidget()
        self.name = QLineEdit("Hmmmm?")
        self.widget_proxy = QGraphicsProxyWidget()
        self.priority = QLineEdit("00")
        self.priority.setValidator(QIntValidator())

    def get_path(self) -> QPainterPath:
        self.get_path = self.straight_path
        return self.straight_path()

    def init_qwidgets(self):

        main_layout = QHBoxLayout()
        self.qwidget.setLayout(main_layout)
        main_layout.addWidget(self.priority)
        main_layout.addWidget(self.name)
        self.widget_proxy.setWidget(self.qwidget)
        self.scene().addItem(self.widget_proxy)
        self.name.setFont(QFont('Times', 6))
        self.priority.setFont(QFont('Times', 6))

        self.widget_proxy.hide()
        self.widget_proxy.setZValue(self.q_line_edit_z)

        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.name.setFixedSize(*self.name_edit_params)
        self.priority.setFixedSize(*self.priority_edit_params)
        self.widget_proxy.setTransformOriginPoint(self.q_line_edit_center)
        self.widget_proxy.setMaximumSize(self.name_edit_params[0] + self.priority_edit_params[0],
                                         self.name_edit_params[1])

    def straight_path(self) -> QPainterPath:
        to_return = QPainterPath(self.from_point)
        to_return.lineTo(self.to_point)
        return to_return

    def set_from_point(self, point: QPointF):
        self.from_point = point
        self.inner_update()

    def set_to_point(self, point: QPointF):
        self.to_point = point
        self.inner_update()

    def inner_update(self):
        path = self.get_path()
        self.setPath(path)
        if path.length() > self.name_edit_params[0] * 2:
            self.widget_proxy.show()
            angle = path.angleAtPercent(0.5)
            rot = (360 - angle) if (angle < 90 or angle > 270) else (180 - angle)
            self.widget_proxy.setRotation(rot)
            self.widget_proxy.setPos(path.pointAtPercent(0.5) - self.q_line_edit_center)
        else:
            self.widget_proxy.hide()

    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionGraphicsItem',
              widget: typing.Optional[QWidget] = ...) -> None:
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        painter.setPen(self.pen)
        painter.drawPath(self.path())

    def shape(self) -> QtGui.QPainterPath:
        qp = QtGui.QPainterPathStroker()
        qp.setWidth(self.width)
        qp.setCapStyle(QtCore.Qt.PenCapStyle.SquareCap)
        shape = qp.createStroke(self.path())
        return shape

    def contextMenuEvent(self, event: 'QGraphicsSceneContextMenuEvent') -> None:
        self.transit.menu_pos = event.pos() if self.transit.custom_map is None else self.transit.custom_map(event.pos())
        self.transit.menu.exec(QPoint(int(event.screenPos().x()), int(event.screenPos().y())))
        event.accept()


@SimpleWidgetWithMenu
class TransitUI:
    @dataclass
    class TransitUIParams:
        point: QPointF
        scene: QGraphicsScene
        state: typing.Any
        create_transit_callback: typing.Callable = None
        update_transit_callback: typing.Callable = None

    def __init__(self, params: TransitUIParams):
        self.path = Line(params.point, params.point, self)
        self.end_circle = Circle(0, 0, 10, 10, Qt.GlobalColor.red, self.path.set_to_point, self)
        self.start_circle = Circle(0, 0, 10, 10, Qt.GlobalColor.darkGreen, self.path.set_from_point, self)

        self.end_circle.setPos(params.point.x() - 5, params.point.y() - 5)
        self.start_circle.setPos(params.point - self.start_circle.center_point)
        self.start_circle.bind_to_stateUI(params.state)
        self.is_created = False

        params.scene.addItem(self.path)
        self.path.init_qwidgets()
        params.scene.addItem(self.end_circle)
        params.scene.addItem(self.start_circle)

        self.create_transit_callback = params.create_transit_callback
        self.update_transit_callback = params.update_transit_callback
        self.name = None
        self.priority = None
        self.transit_id = None

    def to_json(self):
        to_return = {}
        to_return["transit_id"] = self.transit_id
        to_return["transit_name"] = self.name.get()
        to_return["start_point"] = {"x": self.start_circle.scenePos().x(),
                                    "y": self.start_circle.scenePos().y()}
        to_return["end_point"] = {"x": self.end_circle.scenePos().x(),
                                  "y": self.end_circle.scenePos().y()}
        return to_return

    def destroy(self):
        self.path.scene().removeItem(self.path.widget_proxy)
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
        else:
            self.update_transit_callback(self)

    def get_from_state_id(self):
        return self.start_circle.get_state_id()

    def get_to_state_id(self):
        return self.end_circle.get_state_id()

    def set_id(self, id):
        self.transit_id = id

    def set_name(self, name):
        self.name = name
        self.path.name.setText(name.get())
        self.path.name.editingFinished.connect(self.update_name_from_ui)

    def update_name_from_ui(self):
        self.name.set_str(self.path.name.text())

    def get_id(self):
        return self.transit_id

    def get_name(self) -> StrWrapper:
        return self.name

    def set_priority(self, priority):
        self.priority = priority
        self.path.priority.setText(str(priority.get()))
        self.path.priority.editingFinished.connect(self.update_priority_from_ui)

    def update_priority_from_ui(self):
        self.priority.set_int(int(self.path.priority.text()))

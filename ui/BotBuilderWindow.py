from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView

from PathFile import Paths
from ui.SimpleWidgetWithMenu import SimpleWidgetWithMenu
from utils.GetStyleFromFile import get_style


@SimpleWidgetWithMenu
class BotBuilderWindow(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.start_dragging_point = None
        self.init_ui()
        self.transit_thickness = 5
        self.lines_equations = {}
        self.scene_s = QGraphicsScene()
        self.setScene(self.scene_s)
        self.is_moving = False
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.zoom_in_factor = 1.3
        self.zoom_out_factor = 1 / self.zoom_in_factor

    def init_ui(self):
        self.setStyleSheet(get_style(Paths.BotBuilderWindow))

    def add_item(self, item):
        self.scene().addItem(item)

    def add_widget(self, widget):
        return self.scene().addWidget(widget)

    def custom_map(self, point):
        return self.mapToScene(point)

    def contextMenuEvent(self, event):
        super().contextMenuEvent(event)
        return event.isAccepted()

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.MiddleButton and self.itemAt(event.pos()) is None:
            # todo find why it only works before any interaction with UI
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
            self.is_moving = True
            self.start_dragging_point = event.pos()
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        if self.is_moving:
            event.accept()
            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() - (event.pos() - self.start_dragging_point).y())
            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() - (event.pos() - self.start_dragging_point).x())
            self.start_dragging_point = event.pos()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.MiddleButton and self.is_moving:
            self.setCursor(Qt.CursorShape.ArrowCursor)
            self.is_moving = False
            event.accept()
            return
        super().mouseReleaseEvent(event)

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        if event.angleDelta().y() > 0:
            zoom_factor = self.zoom_in_factor
        else:
            zoom_factor = self.zoom_out_factor
        self.scale(zoom_factor, zoom_factor)

from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView

from PathFile import Paths
from ui.SimpleWidgetWithMenu import SimpleWidgetWithMenu
from utils.GetStyleFromFile import get_style
from utils.LinesWrapper import LinesWrapper


@SimpleWidgetWithMenu
class BotBuilderWindow(QGraphicsView):
    # todo implement movement by left click or middle button
    # todo implement area selection and movement
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.lines = LinesWrapper(self.update)
        self.transit_thickness = 5
        self.lines_equations = {}
        self.scene_s = QGraphicsScene()
        self.setScene(self.scene_s)

        def f():
            print("selection changed")
            self.update()
            self.scene_s.update()
        self.scene_s.selectionChanged.connect(f)

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

    def contextMenuEvent(self, event):
        super().contextMenuEvent(event)
        return event.isAccepted()
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

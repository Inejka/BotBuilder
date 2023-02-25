from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView

from PathFile import Paths
from ui.SimpleWidgetWithMenu import SimpleWidgetWithMenu
from utils.GetStyleFromFile import get_style


@SimpleWidgetWithMenu
class BotBuilderWindow(QGraphicsView):
    # todo implement movement by left click or middle button
    # todo implement area selection and movement
    def __init__(self):
        super().__init__()
        self.init_ui()
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

    def custom_map(self, point):
        return self.mapToScene(point)

    def contextMenuEvent(self, event):
        super().contextMenuEvent(event)
        return event.isAccepted()

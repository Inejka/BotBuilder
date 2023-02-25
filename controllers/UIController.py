import json
import os

from PyQt6.QtCore import QPoint, Qt, QPointF
from PyQt6.QtGui import QBrush, QPen
from PyQt6.QtWidgets import QGraphicsItem

from PathFile import Paths
from controllers.MainWindowMenuBarController import MainWindowMenuBarController
from controllers.StateUIController import StateUIController
from controllers.TransitUIController import TransitUIController
from ui.StateUi import StateUI


class UIController:
    def __init__(self, bot, MainWindow):
        self.state_uis = {}
        self.transit_uis = {}
        self.bot = bot
        self.MainWindow = MainWindow
        self.transit_uis_controller = TransitUIController(bot, self.transit_uis, self.MainWindow)
        self.state_uis_controller = StateUIController(bot, self.state_uis, MainWindow, self.try_open_editor)
        self.bind_controllers()
        self.mainWindowMenuBarController = MainWindowMenuBarController(bot, MainWindow, self)
        self.MainWindow.get_bot_builder_window().set_names_with_actions(
            [("Create State", self.state_uis_controller.create_state)])
        self.MainWindow.setGeometry(100, 100, 500, 500)

    def try_open_editor(self, id):
        print(id)
        pass

    def clear(self):
        self.state_uis_controller.clear()
        self.transit_uis_controller.clear()

    def save(self):
        with open(os.path.join(Paths.BotGeneratedFolder, "bot_ui.json"), 'w') as file:
            json.dump(self, file, default=UIController.to_json, indent=4)

    def to_json(self):
        # json loads for bot serialization for not to return a str
        # todo find way to remove json loads
        to_return = '{'
        to_return += '"state_uis":' + json.dumps(self.state_uis, default=StateUI.to_json)
        raise NotImplementedError("Transit Ui")
        to_return += ',"transit_uis":' + json.dumps(self.transit_uis, default=Line.to_json)
        to_return += '}'
        return json.loads(to_return)

    def load(self):
        with open(os.path.join(Paths.BotGeneratedFolder, "bot_ui.json"), 'r') as file:
            self.from_json(json.load(file))

    def from_json(self, parsed_json):
        # todo simplify bot_ui
        # bot_ui -> states from dict to list????????????
        # bot_ui -> transit_uis from dict to list
        for _, i in parsed_json["state_uis"].items():
            self.state_uis_controller.load_state(i)
        for _, i in parsed_json["transit_uis"].items():
            self.transit_uis_controller.load_transit(i, parsed_json["state_uis"])
        self.state_uis_controller.paint_end_start_states()

    def bind_controllers(self):
        self.state_uis_controller.set_transit_uis_controller(self.transit_uis_controller)
        self.transit_uis_controller.set_state_uis_controller(self.state_uis_controller)

import json
import os

from PyQt6.QtCore import QPoint, Qt, QPointF
from PyQt6.QtGui import QBrush, QPen
from PyQt6.QtWidgets import QGraphicsItem

from PathFile import Paths
from controllers.MainWindowMenuBarController import MainWindowMenuBarController
from controllers.StateUIController import StateUIController
from ui.StateUi import StateUI
from utils.LinesWrapper import Point, Line


class UIController:
    def __init__(self, bot, MainWindow):
        self.state_uis = {}
        self.transit_uis = {}
        self.bot = bot
        self.MainWindow = MainWindow
        self.state_uis_controller = StateUIController(bot, self.state_uis, MainWindow, self.try_create_transit,
                                                      self.update_line_equation_by_transit_id, self.try_open_editor)
        self.mainWindowMenuBarController = MainWindowMenuBarController(bot, MainWindow, self)
        self.MainWindow.get_bot_builder_window().set_names_with_actions(
            [("Create State", self.state_uis_controller.create_state)])
        self.MainWindow.setGeometry(100, 100, 500, 500)

    def try_open_editor(self, id):
        print(id)
        pass

    def try_create_transit(self, line: Line):
        # in some cases double left click on stateUi results that line = None
        if line is None:
            return
        to_state_ui = self.get_state_by_point(line[1], line.from_id)
        if to_state_ui is None:
            self.MainWindow.get_bot_builder_window().get_lines_wrapper().remove_line(line)
        else:
            self.create_transit(line, to_state_ui)

    def create_transit(self, line, to_state_ui):
        transit_name, transit_id = self.bot.create_transit(line.from_id, to_state_ui.get_state_id())
        self.state_uis[line.from_id].add_point_with_offset(line[0], Point(line.update_callback,
                                                                          self.state_uis[line.from_id].pos().x() -
                                                                          line[0][0],
                                                                          self.state_uis[line.from_id].pos().y() -
                                                                          line[0][1]))
        to_state_ui.add_point_with_offset(line[1], Point(line.update_callback, to_state_ui.pos().x() - line[1][0],
                                                         to_state_ui.pos().y() - line[1][1]))
        line.set_transit_id(transit_id)
        self.transit_uis[transit_id] = line
        self.update_line_equation_by_transit_id(transit_id)

    def update_line_equation_by_transit_id(self, transit_id):
        line = self.transit_uis[transit_id]
        k = (line[0][1] - line[1][1]) / (line[0][0] - line[1][0]) if not line[0][0] == line[1][0] else 0
        b = line[0][1] - k * line[0][0]
        self.MainWindow.get_bot_builder_window().lines_equations[transit_id] = (k, b)

    def get_state_by_point(self, point: Point, ignore_id: str) -> StateUI:
        for i in self.state_uis.values():
            if i.pos().x() < point[0] < i.pos().x() + i.size().width() and \
                    i.pos().y() < point[1] < i.pos().y() + i.size().height() and \
                    not ignore_id == i.state_id:
                return i
        return None

    def clear(self):
        # todo fix clear
        self.state_uis_controller.clear()
        for key, value in self.transit_uis.items():
            self.MainWindow.get_bot_builder_window().get_lines_wrapper().remove_line(value)
        self.transit_uis.clear()

    def save(self):
        # todo fix state save
        with open(os.path.join(Paths.BotGeneratedFolder, "bot_ui.json"), 'w') as file:
            json.dump(self, file, default=UIController.to_json, indent=4)

    def to_json(self):
        # json loads for bot serialization for not to return a str
        # todo find way to remove json loads
        to_return = '{'
        to_return += '"state_uis":' + json.dumps(self.state_uis, default=StateUI.to_json)
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
            self.load_transit(i, parsed_json["state_uis"])
        self.state_uis_controller.paint_end_start_states()

    def load_transit(self, load_from, state_uis_reference):
        builder = self.MainWindow.get_bot_builder_window()
        lines = builder.get_lines_wrapper()
        line = Line(lines.update_callback, self.bot.get_transit_by_id(load_from["transit_id"]).get_from_state_id(),
                    load_from["from_x"],
                    load_from["from_y"], load_from["to_x"],
                    load_from["to_y"])
        lines.add_line(line)
        self.state_uis[line.from_id].add_point_with_offset(line[0], self.find_point_data_and_create(
            state_uis_reference[self.bot.get_transit_by_id(load_from["transit_id"]).get_from_state_id()],
            load_from["from_x"], load_from["from_y"], lines.update_callback))
        self.state_uis[self.bot.get_transit_by_id(load_from["transit_id"]).get_to_state_id()].add_point_with_offset(
            line[1], self.find_point_data_and_create(
                state_uis_reference[self.bot.get_transit_by_id(load_from["transit_id"]).get_to_state_id()],
                load_from["to_x"], load_from["to_y"], lines.update_callback))
        line.set_transit_id(load_from["transit_id"])
        self.transit_uis[load_from["transit_id"]] = line
        self.update_line_equation_by_transit_id(load_from["transit_id"])

    def find_point_data_and_create(self, state_info, x, y, line_update_callback):
        for i in state_info["point_with_offset"]:
            if i["point"]["x"] == x and i["point"]["y"] == y:
                return Point(line_update_callback, i["offset"]["x"], i["offset"]["y"])

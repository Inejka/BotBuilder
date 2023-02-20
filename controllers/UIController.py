import json
import os

from PathFile import Paths
from controllers.MainWindowMenuBarController import MainWindowMenuBarController
from controllers.StateUIColorController import StateUIColorController
from ui.StateUi import StateUI
from utils.LinesWrapper import Point, Line


class UIController:
    def __init__(self, bot, MainWindow):
        self.state_uis = {}
        self.transit_uis = {}
        self.bot = bot
        self.MainWindow = MainWindow
        self.stateUIColorController = StateUIColorController(bot, self.state_uis)
        self.mainWindowMenuBarController = MainWindowMenuBarController(bot, MainWindow, self)
        self.MainWindow.get_bot_builder_window().get_inner_widget().set_names_with_actions(
            [("Create State", self.create_state)])

    def create_state(self):
        state_name, state_id = self.bot.create_state()
        builder = self.MainWindow.get_bot_builder_window()
        state_ui = StateUI(builder.get_inner_widget(), state_name, builder.get_lines_wrapper(), state_id,
                           self.try_create_transit, self.update_line_equation_by_transit_id, self.try_open_editor)
        state_ui.set_names_with_actions([("Set start", self.stateUIColorController.set_start_state, state_ui),
                                         ("Add end", self.stateUIColorController.add_end_state, state_ui),
                                         ("Remove end", self.stateUIColorController.remove_end_state, state_ui)])
        state_ui.move(self.MainWindow.get_bot_builder_window().get_inner_widget().get_menu_pos())
        self.state_uis[state_id] = state_ui

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
        for key, value in self.state_uis.items():
            value.deleteLater()
        for key, value in self.transit_uis.items():
            self.MainWindow.get_bot_builder_window().get_lines_wrapper().remove_line(value)
        self.state_uis = {}
        self.transit_uis = {}

    def save(self):
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

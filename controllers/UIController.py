import json
import os
import subprocess

from bot.Bot import Bot
from controllers.MainWindowMenuBarController import MainWindowMenuBarController
from controllers.StateUIController import StateUIController
from controllers.TransitUIController import TransitUIController
from PathFile import Paths
from ui.MainWindow import MainWindow
from ui.StateUi import StateUI
from ui.TransitUI import TransitUI


class UIController:
    def __init__(self, bot: Bot, main_window: MainWindow) -> None:
        self.state_uis = {}
        self.transit_uis = {}
        self.bot = bot
        self.MainWindow = main_window
        self.transit_uis_controller = TransitUIController(bot, self.transit_uis, self.MainWindow, self.try_open_editor)
        self.state_uis_controller = StateUIController(bot, self.state_uis, main_window, self.try_open_editor)
        self.bind_controllers()
        self.mainWindowMenuBarController = MainWindowMenuBarController(bot, main_window, self)
        self.MainWindow.get_bot_builder_window().set_names_with_actions(
            [("Create State", self.state_uis_controller.create_state)])
        self.MainWindow.setGeometry(100, 100, 500, 500)

    def try_open_editor(self, file_path: str) -> None:
        subprocess.run([Paths.IDE, file_path])

    def clear(self) -> None:
        self.state_uis_controller.clear()
        self.transit_uis_controller.clear()

    def save(self) -> None:
        with open(os.path.join(Paths.BotGeneratedFolder, "bot_ui.json"), "w") as file:
            json.dump(self, file, default=UIController.to_json, indent=4)

    def to_json(self) -> dict:
        # json loads for bot serialization for not to return a str
        # todo find way to remove json loads
        to_return = "{"
        to_return += '"state_uis":' + json.dumps(self.state_uis, default=StateUI.to_json)
        to_return += ',"transit_uis":' + json.dumps(self.transit_uis, default=TransitUI.to_json)
        to_return += "}"
        return json.loads(to_return)

    def load(self) -> None:
        with open(os.path.join(Paths.BotGeneratedFolder, "bot_ui.json")) as file:
            self.from_json(json.load(file))

    def from_json(self, parsed_json: dict) -> None:
        # todo simplify bot_ui
        # bot_ui -> states from dict to list????????????
        # bot_ui -> transit_uis from dict to list
        for _, i in parsed_json["state_uis"].items():
            self.state_uis_controller.load_state(i)
        for _, i in parsed_json["transit_uis"].items():
            self.transit_uis_controller.load_transit(i)
        self.state_uis_controller.paint_end_start_states()

    def bind_controllers(self) -> None:
        self.state_uis_controller.set_transit_uis_controller(self.transit_uis_controller)
        self.transit_uis_controller.set_state_uis_controller(self.state_uis_controller)

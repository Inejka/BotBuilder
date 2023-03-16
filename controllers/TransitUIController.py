import typing
from typing import TYPE_CHECKING

from PyQt6.QtCore import QPointF

if TYPE_CHECKING:
    from bot.Bot import Bot
    from controllers.StateUIController import StateUIController
    from ui.MainWindow import MainWindow
from ui.TransitUI import TransitUI
from utils.IntWrapper import IntWrapper
from utils.StrWrapper import StrWrapper


class TransitUIController:
    def __init__(self, bot: "Bot", transit_uis: dict, main_window: "MainWindow",
                 try_open_editor: typing.Callable) -> None:
        self.bot = bot
        self.transit_uis = transit_uis
        self.main_window = main_window
        self.state_uis_controller = None
        self.try_open_editor_callback = try_open_editor

    def create_transit(self, transit_ui: TransitUI) -> None:
        transit_name, transit_id, transit_priority = self.bot.create_transit(transit_ui.get_from_state_id(),
                                                                             transit_ui.get_to_state_id())
        self.finish_transit_ui_init(transit_ui, transit_id, transit_name, transit_priority)

    def try_open_editor(self, inner_id: str) -> None:
        self.try_open_editor_callback(self.bot.get_transit_by_id(inner_id).get_associated_file())

    def load_transit(self, load_from: dict) -> None:
        transit_id = load_from["transit_id"]
        bot_transit = self.bot.get_transit_by_id(transit_id)
        transit_name = bot_transit.get_name()
        transit_priority = bot_transit.get_priority()
        from_state_id = bot_transit.get_from_state_id()
        to_state_id = bot_transit.get_to_state_id()

        transit_ui = self.generate_transit_ui(
            TransitUI.TransitUIParams(QPointF(0, 0), self.state_uis_controller.state_uis[
                from_state_id].get_proxy().scene(), self.state_uis_controller.state_uis[from_state_id]))
        transit_ui.is_created = True
        transit_ui.start_circle.setParentItem(None)
        transit_ui.start_circle.setPos(QPointF(load_from["start_point"]["x"], load_from["start_point"]["y"]))
        transit_ui.end_circle.setPos(QPointF(load_from["end_point"]["x"], load_from["end_point"]["y"]))
        transit_ui.end_circle.bind_to_stateUI(self.state_uis_controller.state_uis[to_state_id])
        transit_ui.start_circle.bind_to_stateUI(self.state_uis_controller.state_uis[from_state_id])

        self.finish_transit_ui_init(transit_ui, transit_id, transit_name, transit_priority)

    def finish_transit_ui_init(self, transit_ui: "TransitUI", transit_id: str, transit_name: StrWrapper,
                               transit_priority: IntWrapper) -> None:
        transit_ui.set_name(transit_name)
        transit_ui.set_priority(transit_priority)
        transit_ui.set_id(transit_id)
        self.transit_uis[transit_id] = transit_ui

    def update_transit_from_ui(self, transit_ui: TransitUI) -> None:
        transit = self.bot.get_transit_by_id(transit_ui.get_id())
        if transit.get_to_state_id() != transit_ui.get_to_state_id():
            transit.set_to_state(self.bot.get_state_by_id(transit_ui.get_to_state_id()))
            return
        if transit.get_from_state_id() != transit_ui.get_from_state_id():
            self.bot.get_state_by_id(transit.get_from_state_id()).remove_transit(transit)
            self.bot.get_state_by_id(transit_ui.get_from_state_id()).add_transit(transit)
            transit.set_from_state(self.bot.get_state_by_id(transit_ui.get_from_state_id()))
            return

    def set_state_uis_controller(self, state_uis_controller: "StateUIController") -> None:
        self.state_uis_controller = state_uis_controller

    def clear(self) -> None:
        for _, value in self.transit_uis.items():
            value.destroy()
        self.transit_uis.clear()

    def generate_transit_ui(self, params: TransitUI.TransitUIParams) -> TransitUI:
        params.update_transit_callback = self.update_transit_from_ui
        params.create_transit_callback = self.create_transit
        params.try_open_editor_callback = self.try_open_editor
        transit_ui = TransitUI(params)
        transit_ui.set_names_with_actions([("Remove transit", self.remove_transit, transit_ui)])
        return transit_ui

    def remove_transit(self, transit_ui: TransitUI) -> None:
        self.bot.remove_transit_by_id(transit_ui.get_id())
        self.transit_uis.pop(transit_ui.get_id())
        transit_ui.destroy()

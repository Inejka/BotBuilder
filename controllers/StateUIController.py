from collections.abc import Callable

from PyQt6.QtCore import QPointF

from bot.Bot import Bot
from controllers.StateUIColorController import StateUIColorController
from ui.BotBuilderWindow import BotBuilderWindow
from ui.MainWindow import MainWindow
from ui.StateUi import ControlRectangle, StateUI, StateUIProxy
from utils.StrWrapper import StrWrapper


class StateUIController:
    def __init__(self, bot: Bot, state_uis: dict, main_window: MainWindow, try_open_editor: Callable) -> None:
        self.bot = bot
        self.mainWindow = main_window
        self.state_uis = state_uis
        self.try_open_editor = try_open_editor
        self.stateUIColorController = StateUIColorController(bot, self.state_uis)
        self.transit_uis_controller = None

    def create_state(self) -> None:
        state_name, state_id = self.bot.create_state()
        builder = self.mainWindow.get_bot_builder_window()
        self.initialize_state(builder, state_id, state_name, builder.get_menu_pos())

    def initialize_state(self, builder: BotBuilderWindow, state_id: str, state_name: StrWrapper,
                         point: QPointF) -> None:
        state_ui = StateUI(StateUI.StateUIParams(state_name, state_id, self.try_open_editor,
                                                 self.transit_uis_controller.generate_transit_ui))
        state_ui.set_names_with_actions([("Set start", self.stateUIColorController.set_start_state, state_ui),
                                         ("Add end", self.stateUIColorController.add_end_state, state_ui),
                                         ("Remove end", self.stateUIColorController.remove_end_state, state_ui),
                                         ("Remove state", self.remove_state, state_ui)])
        self.create_control_proxy_and_bind(builder, point, state_ui)
        self.state_uis[state_id] = state_ui

    def create_control_proxy_and_bind(self, builder: BotBuilderWindow, point: QPointF, state_ui: StateUI) -> None:
        proxy = StateUIProxy(state_ui)
        proxy.setPos(point)
        proxy_control = ControlRectangle(state_ui.width() + 1, state_ui, state_ui.height() + 10)
        proxy.setParentItem(proxy_control)
        proxy.setPos(1, proxy_control.rect().height() - state_ui.height())
        proxy_control.setPos(point)
        builder.add_item(proxy_control)
        state_ui.bind_proxies(proxy_control, proxy)

    def load_state(self, load_from: dict) -> None:
        builder = self.mainWindow.get_bot_builder_window()
        self.initialize_state(builder, load_from["state_id"],
                              self.bot.get_name_wrapper_by_state_id(load_from["state_id"]),
                              QPointF(load_from["pos_x"], load_from["pos_y"]))

    def paint_end_start_states(self) -> None:
        if self.bot.get_start_state() is not None:
            self.stateUIColorController.paint_start_state(self.state_uis[self.bot.get_start_state()])
        for i in self.bot.get_end_states():
            self.stateUIColorController.paint_end_state(self.state_uis[i])

    def clear(self) -> None:
        for _key, value in self.state_uis.items():
            value.destroy()
        self.state_uis.clear()

    def set_transit_uis_controller(self, transit_uis_controller: "TransitUIController") -> None:
        # can't import TransitUIController due to circular import, yeah
        self.transit_uis_controller = transit_uis_controller

    def get_state_by_id(self, state_id: str) -> StateUI:
        return self.state_uis[state_id]

    def remove_state(self, state_ui: StateUI) -> None:
        to_remove = self.bot.get_associated_transit_by_state_id(state_ui.get_state_id())
        to_remove = list(to_remove["starts"]) + list(to_remove["ends"])
        to_remove = [x for x in self.transit_uis_controller.transit_uis.values() if x.get_id() in to_remove]
        for to_delete_transit in to_remove:
            self.transit_uis_controller.remove_transit(to_delete_transit)
        self.bot.remove_state_by_id(state_ui.get_state_id())
        self.state_uis.pop(state_ui.get_state_id())
        state_ui.destroy()

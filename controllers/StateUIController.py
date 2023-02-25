from PyQt6.QtCore import QPointF

from controllers.StateUIColorController import StateUIColorController
from ui.StateUi import StateUI, ControlRectangle, StateUIProxy
from utils.LinesWrapper import Point


class StateUIController:
    def __init__(self, bot, state_uis, mainWindow, try_open_editor):
        self.bot = bot
        self.mainWindow = mainWindow
        self.state_uis = state_uis
        self.try_open_editor = try_open_editor
        self.stateUIColorController = StateUIColorController(bot, self.state_uis)
        self.transit_uis_controller = None

    def create_state(self):
        state_name, state_id = self.bot.create_state()
        builder = self.mainWindow.get_bot_builder_window()
        self.initialize_state(builder, state_id, state_name, builder.get_menu_pos())

    def initialize_state(self, builder, state_id, state_name, point):
        state_ui = StateUI(state_name, builder.get_lines_wrapper(), state_id,
                           self.transit_uis_controller.try_create_transit,
                           self.transit_uis_controller.update_line_equation_by_transit_id, self.try_open_editor)
        state_ui.set_names_with_actions([("Set start", self.stateUIColorController.set_start_state, state_ui),
                                         ("Add end", self.stateUIColorController.add_end_state, state_ui),
                                         ("Remove end", self.stateUIColorController.remove_end_state, state_ui)])
        self.create_control_proxy_and_bind(builder, point, state_ui)
        self.state_uis[state_id] = state_ui

    def create_control_proxy_and_bind(self, builder, point, state_ui):
        proxy = StateUIProxy(state_ui)
        proxy.setPos(point)
        proxyControl = ControlRectangle(state_ui.width() + 1, state_ui, state_ui.height() + 10)
        proxy.setParentItem(proxyControl)
        proxy.setPos(1, proxyControl.rect().height() - state_ui.height())
        proxyControl.setPos(point)
        builder.add_item(proxyControl)
        state_ui.bind_proxies(proxyControl, proxy)

    def load_state(self, load_from):
        builder = self.mainWindow.get_bot_builder_window()
        self.initialize_state(builder, load_from["state_id"],
                              self.bot.get_name_wrapper_by_state_id(load_from["state_id"]),
                              QPointF(load_from["pos_x"], load_from["pos_y"]))

    def paint_end_start_states(self):
        if self.bot.get_start_state() is not None:
            self.stateUIColorController.paint_start_state(self.state_uis[self.bot.get_start_state()])
        for i in self.bot.get_end_states():
            self.stateUIColorController.paint_end_state(self.state_uis[i])

    def clear(self):
        builder = self.mainWindow.get_bot_builder_window()
        for key, value in self.state_uis.items():
            value.deleteLater()
            builder.scene().removeItem(value.get_control_proxy())
        self.state_uis.clear()

    def get_state_by_point(self, point: Point, ignore_id: str) -> StateUI:
        for i in self.state_uis.values():
            if i.pos().x() < point[0] < i.pos().x() + i.size().width() and \
                    i.pos().y() < point[1] < i.pos().y() + i.size().height() and \
                    not ignore_id == i.state_id:
                return i
        return None

    def set_transit_uis_controller(self, transit_uis_controller):
        self.transit_uis_controller = transit_uis_controller

    def get_state_by_id(self, state_id: str) -> StateUI:
        return self.state_uis[state_id]

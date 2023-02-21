from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QBrush, QPen
from PyQt6.QtWidgets import QGraphicsItem

from controllers.StateUIColorController import StateUIColorController
from ui.StateUi import StateUI


class StateUIController:
    def __init__(self, bot, state_uis, mainWindow, try_create_transit, update_line_equation_by_transit_id,
                 try_open_editor):
        self.bot = bot
        self.mainWindow = mainWindow
        self.state_uis = state_uis
        self.try_create_transit = try_create_transit
        self.update_line_equation_by_transit_id = update_line_equation_by_transit_id
        self.try_open_editor = try_open_editor
        self.stateUIColorController = StateUIColorController(bot, self.state_uis)

    def create_state(self):
        state_name, state_id = self.bot.create_state()
        builder = self.mainWindow.get_bot_builder_window()
        self.initialize_state(builder, state_id, state_name, builder.get_menu_pos())

    def initialize_state(self, builder, state_id, state_name, point):
        state_ui = StateUI(state_name, builder.get_lines_wrapper(), state_id, self.try_create_transit,
                           self.update_line_equation_by_transit_id, self.try_open_editor)
        state_ui.set_names_with_actions([("Set start", self.stateUIColorController.set_start_state, state_ui),
                                         ("Add end", self.stateUIColorController.add_end_state, state_ui),
                                         ("Remove end", self.stateUIColorController.remove_end_state, state_ui)])
        self.create_control_proxy_and_bind(builder, point, state_ui)
        self.state_uis[state_id] = state_ui

    def create_control_proxy_and_bind(self, builder, point, state_ui):
        proxy = builder.add_widget(state_ui)
        proxy.setPos(point)
        proxyControl = builder.scene().addRect(0, 0, state_ui.width(), 20, QPen(Qt.GlobalColor.black),
                                               QBrush(Qt.GlobalColor.darkGreen))
        proxyControl.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        proxyControl.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        proxy.setParentItem(proxyControl)
        proxy.setPos(0, proxyControl.rect().height())
        proxyControl.setPos(point)
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
        for key, value in self.state_uis.items():
            value.deleteLater()
        self.state_uis.clear()

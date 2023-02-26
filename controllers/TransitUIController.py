from PyQt6.QtCore import QPointF

from ui.TransitUI import TransitUI


class TransitUIController:
    def __init__(self, bot, transit_uis, MainWindow):
        self.bot = bot
        self.transit_uis = transit_uis
        self.MainWindow = MainWindow
        self.state_uis_controller = None

    def create_transit(self, transitUi: TransitUI):
        transit_name, transit_id = self.bot.create_transit(transitUi.get_from_state_id(), transitUi.get_to_state_id())
        self.finish_TransitUi_init(transitUi, transit_id, transit_name)

    def load_transit(self, load_from):
        transit_id = load_from["transit_id"]
        bot_transit = self.bot.get_transit_by_id(transit_id)
        transit_name = bot_transit.get_name()
        from_state_id = bot_transit.get_from_state_id()
        to_state_id = bot_transit.get_to_state_id()

        transitUi = TransitUI(QPointF(0, 0), self.state_uis_controller.state_uis[from_state_id].get_proxy().scene(),
                              self.state_uis_controller.state_uis[from_state_id], self.create_transit)
        transitUi.is_created = True
        transitUi.start_circle.setParentItem(None)
        transitUi.start_circle.setPos(QPointF(load_from["start_point"]["x"], load_from["start_point"]["y"]))
        transitUi.end_circle.setPos(QPointF(load_from["end_point"]["x"], load_from["end_point"]["y"]))
        transitUi.end_circle.bind_to_stateUI(self.state_uis_controller.state_uis[to_state_id])
        transitUi.start_circle.bind_to_stateUI(self.state_uis_controller.state_uis[from_state_id])

        self.finish_TransitUi_init(transitUi, transit_id, transit_name)

    def finish_TransitUi_init(self, transitUi, transit_id, transit_name):
        transitUi.set_name(transit_name)
        transitUi.set_id(transit_id)
        self.transit_uis[transit_id] = transitUi

    def set_state_uis_controller(self, state_uis_controller):
        self.state_uis_controller = state_uis_controller

    def clear(self):
        for _, value in self.transit_uis.items():
            value.destroy()
        self.transit_uis.clear()

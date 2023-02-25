from ui.TransitUI import TransitUI


class TransitUIController:
    def __init__(self, bot, transit_uis, MainWindow):
        self.bot = bot
        self.transit_uis = transit_uis
        self.MainWindow = MainWindow
        self.state_uis_controller = None

    def create_transit(self, transitUi: TransitUI):
        transit_name, transit_id = self.bot.create_transit(transitUi.get_from_state_id(), transitUi.get_to_state_id())
        transitUi.set_name(transit_name)
        transitUi.set_id(transit_id)
        self.transit_uis[transit_id] = transitUi

    def load_transit(self, load_from, state_uis_reference):
        raise NotImplementedError("load_transit")
        # builder = self.MainWindow.get_bot_builder_window()
        # lines = builder.get_lines_wrapper()
        # line = Line(lines.update_callback, self.bot.get_transit_by_id(load_from["transit_id"]).get_from_state_id(),
        #             load_from["from_x"],
        #             load_from["from_y"], load_from["to_x"],
        #             load_from["to_y"])
        # lines.add_line(line)
        # self.state_uis_controller.get_state_by_id(line.from_id).add_point_with_offset(line[0],
        #                                                                               self.find_point_data_and_create(
        #                                                                                   state_uis_reference[
        #                                                                                       self.bot.get_transit_by_id(
        #                                                                                           load_from[
        #                                                                                               "transit_id"]).get_from_state_id()],
        #                                                                                   load_from["from_x"],
        #                                                                                   load_from["from_y"],
        #                                                                                   lines.update_callback))
        # self.state_uis_controller.get_state_by_id(
        #     self.bot.get_transit_by_id(load_from["transit_id"]).get_to_state_id()).add_point_with_offset(
        #     line[1], self.find_point_data_and_create(
        #         state_uis_reference[self.bot.get_transit_by_id(load_from["transit_id"]).get_to_state_id()],
        #         load_from["to_x"], load_from["to_y"], lines.update_callback))
        # line.set_transit_id(load_from["transit_id"])
        # self.transit_uis[load_from["transit_id"]] = line

    def find_point_data_and_create(self, state_info, x, y, line_update_callback):
        raise NotImplementedError("In refactor")

    def set_state_uis_controller(self, state_uis_controller):
        self.state_uis_controller = state_uis_controller

    def clear(self):
        for _, value in self.transit_uis.items():
            value.destroy()
        self.transit_uis.clear()

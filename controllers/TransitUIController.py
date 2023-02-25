from utils.LinesWrapper import Line, Point


class TransitUIController:
    def __init__(self, bot, transit_uis, MainWindow):
        self.bot = bot
        self.transit_uis = transit_uis
        self.MainWindow = MainWindow
        self.state_uis_controller = None

    def try_create_transit(self, line: Line):
        # in some cases double left click on stateUi results that line = None
        if line is None:
            return
        to_state_ui = self.state_uis_controller.get_state_by_point(line[1], line.from_id)
        if to_state_ui is None:
            self.MainWindow.get_bot_builder_window().get_lines_wrapper().remove_line(line)
        else:
            self.create_transit(line, to_state_ui)

    def create_transit(self, line, to_state_ui):
        transit_name, transit_id = self.bot.create_transit(line.from_id, to_state_ui.get_state_id())
        self.state_uis_controller.get_state_by_id(line.from_id).add_point_with_offset(line[0],
                                                                                      Point(line.update_callback,
                                                                                            self.state_uis_controller.get_state_by_id(
                                                                                                line.from_id).pos().x() -
                                                                                            line[0][0],
                                                                                            self.state_uis_controller.get_state_by_id(
                                                                                                line.from_id).pos().y() -
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

    def load_transit(self, load_from, state_uis_reference):
        builder = self.MainWindow.get_bot_builder_window()
        lines = builder.get_lines_wrapper()
        line = Line(lines.update_callback, self.bot.get_transit_by_id(load_from["transit_id"]).get_from_state_id(),
                    load_from["from_x"],
                    load_from["from_y"], load_from["to_x"],
                    load_from["to_y"])
        lines.add_line(line)
        self.state_uis_controller.get_state_by_id(line.from_id).add_point_with_offset(line[0],
                                                                                      self.find_point_data_and_create(
                                                                                          state_uis_reference[
                                                                                              self.bot.get_transit_by_id(
                                                                                                  load_from[
                                                                                                      "transit_id"]).get_from_state_id()],
                                                                                          load_from["from_x"],
                                                                                          load_from["from_y"],
                                                                                          lines.update_callback))
        self.state_uis_controller.get_state_by_id(
            self.bot.get_transit_by_id(load_from["transit_id"]).get_to_state_id()).add_point_with_offset(
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

    def set_state_uis_controller(self, state_uis_controller):
        self.state_uis_controller = state_uis_controller

    def clear(self):
        for key, value in self.transit_uis.items():
            self.MainWindow.get_bot_builder_window().get_lines_wrapper().remove_line(value)
        self.transit_uis.clear()

from bot.Bot import Bot
from ui.StateUi import StateUI
from ui.UiInitializer import initialize_ui
from utils.LinesWrapper import Line, LinesWrapper, Point


class MainController:
    def __init__(self):
        self.app = None
        self.bot = None
        self.MainWindow = None
        self.state_uis = {}
        self.KOSTYA_transit_id_to_line = {}
        self.commands = {"hi": self.add_hello_world}

    def print_line(self, to_print: str):
        pass

    def start(self):
        self.app, self.MainWindow = initialize_ui()
        self.bot = Bot()
        self.MainWindow.get_bot_builder_window().get_inner_widget().set_names_with_actions(
            [("Create State", self.create_state)])
        self.print_line = self.MainWindow.get_central_widget().get_command_line().get_output().add_text
        self.MainWindow.get_central_widget().get_command_line().get_input().set_commands(self.commands)
        self.app.exec()

    def create_state(self):
        state_name, state_id, state_file = self.bot.create_state()
        builder = self.MainWindow.get_bot_builder_window()
        state_ui = StateUI(builder.get_inner_widget(), state_name, builder.get_x_offset, builder.get_y_offset,
                           builder.get_lines_wrapper(), state_id, self.try_create_transit,
                           self.update_line_equation_by_transit_id,state_file )
        state_ui.move(self.MainWindow.get_bot_builder_window().get_inner_widget().menu.pos().x(),
                      self.MainWindow.get_bot_builder_window().get_inner_widget().menu.pos().y())
        self.state_uis[state_id] = state_ui

        self.MainWindow.get_bot_builder_window().get_inner_widget().menu.setParent(None)
        self.MainWindow.get_bot_builder_window().get_inner_widget().menu = None

    def try_create_transit(self, line: Line):
        if line is None:
            return
        to_state_ui = self.get_state_by_point(line[1], line.from_id)

        if to_state_ui is None:
            self.MainWindow.get_bot_builder_window().get_lines_wrapper().remove_line(line)
        else:
            transit_name, transit_id = self.bot.create_transit(line.from_id, to_state_ui.get_state_id())
            self.state_uis[line.from_id].add_point_with_offset(line[0], Point(line.update_callback,
                                                                              self.state_uis[line.from_id].pos().x() -
                                                                              line[0][0],
                                                                              self.state_uis[line.from_id].pos().y() -
                                                                              line[0][1]))
            to_state_ui.add_point_with_offset(line[1], Point(line.update_callback, to_state_ui.pos().x() - line[1][0],
                                                             to_state_ui.pos().y() - line[1][1]))
            line.set_transit_id(transit_id)
            self.KOSTYA_transit_id_to_line[transit_id] = line
            self.update_line_equation_by_transit_id(transit_id)

    def update_line_equation_by_transit_id(self, transit_id):
        line = self.KOSTYA_transit_id_to_line[transit_id]
        k = (line[0][1] - line[1][1]) / (line[0][0] - line[1][0])
        b = line[0][1] - k * line[0][0]
        self.MainWindow.get_bot_builder_window().lines_equations[transit_id] = (k, b)

    def get_state_by_point(self, point: Point, ignore_id: str) -> StateUI:
        for i in self.state_uis.values():
            if i.pos().x() < point[0] < i.pos().x() + i.size().width() and \
                    i.pos().y() < point[1] < i.pos().y() + i.size().height() and \
                    not ignore_id == i.state_id:
                return i
        return None

    def add_hello_world(self):
        self.print_line("Hello world")

import command_line.Commands as Commands
from command_line.Commands import Command
from controllers import MainController
from factories.CommandLineCommandFactory import create_command
import importlib


class CommandLineController:
    def __init__(self, main_controller: MainController):
        self.commands = {}
        for cls in Command.__subclasses__():
            command = create_command(cls.__name__, main_controller)
            self.commands[command.get_command_name()] = command.exec
        main_controller.get_main_window().get_central_widget().get_command_line().get_input().set_commands(
            self.commands)

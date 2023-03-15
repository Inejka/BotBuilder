from PyQt6.QtWidgets import QApplication

from ui.CommandLine import CommandLineOutput


class Command:
    def get_command_name(self) -> str:
        pass

    def exec(self) -> None:
        pass


class HiCommand(Command):

    def __init__(self, command_line_output: CommandLineOutput) -> None:
        self.command_line_output = command_line_output

    def get_command_name(self) -> str:
        return "Hi"

    def exec(self) -> None:
        self.command_line_output.add_text("Hi world")


class CloseCommand(Command):

    def __init__(self, to_close: QApplication) -> None:
        self.to_close = to_close

    def get_command_name(self) -> str:
        return "Close"

    def exec(self) -> None:
        self.to_close.closeAllWindows()

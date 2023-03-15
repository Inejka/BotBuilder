from command_line.Commands import CloseCommand, Command, HiCommand
from controllers import MainController


def create_command(class_name: str, main_controller: MainController = None) -> Command:
    match class_name:
        case "HiCommand":
            return HiCommand(main_controller.get_main_window().get_central_widget().get_command_line().get_output())
        case "CloseCommand":
            return CloseCommand(main_controller.app)
            pass
    raise NotImplementedError(class_name)
